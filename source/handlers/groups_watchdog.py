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

    async def __like(self, token: Token, group: Group, post: Post, delay: int) -> bool:
        sleep(delay)
        try:
            vk = Vk(token=token.content)
            vk.like(group.id, post.id)
            return True
        except ApiError as e:
            if e.error.get('error_code') == 5:  # Invalid token
                self.__db_tokens.delete(token)
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

        for group in self.__groups:
            self.__bind_likes(group_id=group.id)

        self.__bind_users()
        tasks = []
        loop = Utils.get_event_loop()
        asyncio.set_event_loop(loop)

        for group in self.__db_groups.get():
            for post in group.posts:
                users_not_liked = [user for user in self.__users if
                                   user.id not in [x.user_id for x in post.likes] and user.token]
                random.shuffle(users_not_liked)

                if len(users_not_liked) > 0:
                    will_handled = random.randint(1, len(users_not_liked))
                    for user in users_not_liked:
                        tasks.append(self.__like(user.token, group, post, random.randint(5, 120)))

                        if len(tasks) == will_handled:
                            break

                    loop.run_until_complete(asyncio.wait(tasks))
                    tasks.clear()

    def run(self) -> None:
        while True:
            self.__routine()
            sleep(30)
