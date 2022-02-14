from vk_api import VkApi
from core import vk_config

from source.database.models import Post, Like


class Vk:
    def __init__(self, token=vk_config['service_key']):
        self.vk = VkApi(token=token)

    def who_am_i(self) -> dict:
        return self.vk.method('users.get')[0]

    def get_group_posts(self, owner_id: int, count=20, offset=0) -> list:
        raw_posts = self.vk.method('wall.get', {
            'owner_id': owner_id,
            'offset': offset,
            'count': count
        })

        posts = []
        for raw_post in raw_posts['items']:
            post_id = raw_post['id']
            post = Post(id=post_id, group_id=owner_id)
            posts.append(post)

        return posts

    def like(self, owner_id: int, item_id: int, type='post') -> None:
        self.vk.method('likes.add', {
            'type': type,
            'owner_id': owner_id,
            'item_id': item_id
        })

    def get_likes(self, owner_id: int, item_id: int, filter='likes', extended=0, type='post') -> list:
        raw_likes = self.vk.method('likes.getList', {
            'type': type,
            'owner_id': owner_id,
            'item_id': item_id,
            'filter': filter,
            'extended': extended
        })

        likes = []

        for raw_like in raw_likes['items']:
            like = Like(post_id=item_id, user_id=raw_like)
            likes.append(like)

        return likes
