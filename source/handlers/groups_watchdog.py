from source.api import Vk
from source.database.methods import *
from source.database.models import *
from source.database import Session

from time import sleep
from threading import Thread


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

        for group in self.__groups:
             for post in group.posts:
                users_not_liked = [user for user in self.__users if user.id not in [x.user_id for x in post.likes] and user.token]
                for user in users_not_liked:
                    try:
                        vk = Vk(token=user.token.content, proxy=True)
                        vk.like(group.id, post.id)
                        sleep(1)
                    except Exception as e:
                        self.__db_tokens.remove(user.token)

    def run(self) -> None:
        while True:
            self.__routine()
            sleep(30)
