from time import sleep
from threading import Thread
from vk_api import ApiError
import asyncio
import random

from source.api import Vk
from source.database.methods import *
from source.database.models import *
from source.database import Session
from source.utils import Utils
from core import *
from source.utils import LoggerFactory


class GroupsWatchDog(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__groups = []
        self.__users = []
        self.__db_session = Session()
        self.__db_groups = GroupMethods(session=self.__db_session)
        self.__db_posts = PostMethods(session=self.__db_session)
        self.__db_likes = LikeMethods(session=self.__db_session)
        self.__db_users = UserMethods(session=self.__db_session)
        self.__db_tokens = TokenMethods(session=self.__db_session)
        self.__service_vk = Vk()
        self.__logger = LoggerFactory.get_logger(GroupsWatchDog.__name__)
        self.__epoch_delay = engine_config['epoch_delay']
        self.__task_delay = engine_config['task_delay']

    async def __like(self, token: Token, group: Group, post: Post, delay: int) -> bool:
        await asyncio.sleep(delay)
        if not self.__db_tokens.get(uid=token.uid):  # User unsubscribed, but task is exists
            return False
        try:
            vk = Vk(token=token.get_decoded_content())
            vk.like(group.id, post.id)
            return True
        except ApiError as e:
            self.__logger.warning(f'Something went wrong with user_id: {token.user_id}.\n{str(e)}')
            if e.error.get('error_code') == 5:  # Invalid token
                self.__logger.warning(f'I will disable token for user_id: {token.user_id} cause of 5')
                self.__db_tokens.disable(token)
            elif e.error.get('error_code') == 18:
                self.__logger.warning(f'I will disable token for user_id: {token.user_id} cause of 18')
                self.__db_tokens.disable(token)
            return False
        except Exception as e:
            self.__logger.error(f'Something went wrong with "like" coroutine.\n{e}')
            return False

    def __bind_groups(self) -> None:
        self.__groups = self.__db_groups.get()

    def __bind_users(self) -> None:
        self.__users = self.__db_users.get()

    def __bind_likes(self, group_id: int) -> None:
        posts = self.__service_vk.get_group_posts(group_id)

        for post in posts:
            if not self.__db_posts.exists(id=post.id):
                self.__db_posts.add(post)

            likes = self.__service_vk.get_likes(post.group_id, post.id)

            for like in likes:
                if not self.__db_users.exists(id=like.user_id):
                    self.__db_users.add(User(id=like.user_id))

                if not self.__db_likes.exists(user_id=like.user_id, post_id=post.id):
                    self.__db_likes.add(like)

    def __routine(self) -> None:
        self.__bind_groups()
        [self.__bind_likes(group_id=x.id) for x in self.__groups]
        self.__bind_users()

        self.__logger.debug('Info bound')

        tasks = []
        loop = Utils.get_event_loop()

        for group in self.__db_groups.get():
            for post in group.posts:
                users_not_liked = [user for user in self.__users if
                                   user.id not in [x.user_id for x in
                                                   post.likes] and user.token and user.token.dl is False]
                random.shuffle(users_not_liked)

                if len(users_not_liked) > 0:
                    for user in users_not_liked:
                        # Will like post with some random delay
                        task = loop.create_task(
                            self.__like(user.token, group, post, random.randint(*self.__task_delay)))
                        task.set_name(f'Like -> user_id: {user.id} | post_id: {post.id}')
                        tasks.append(task)

        if tasks:
            loop.run_until_complete(asyncio.wait(tasks))
            tasks.clear()

        loop.close()

    def run(self) -> None:
        retries = 0
        self.__logger.info('Work started')
        while True:
            try:
                self.__logger.info(f'Outdated likes cleared: {self.__db_likes.delete_old()}')
                self.__logger.info(f'Outdated posts cleared: {self.__db_posts.delete_old()}')
                self.__logger.info(f'Outdated users cleared: {self.__db_users.delete_old()}')

                self.__routine()
                retries = 0
            except Exception as e:
                self.__logger.error(f'Something went wrong with routine:\n{str(e)}')
                if retries == 3:
                    self.__logger.fatal('Tried to restart routine 3 times. Shutting down...')
                    exit(-1)
                retries += 1
            sleep(self.__epoch_delay)
