from .base_methods import BaseMethod
from .. import Session
from ..models import Post
from datetime import datetime, timedelta
from core import engine_config


class PostMethods(BaseMethod):
    def __init__(self, session=Session()):
        BaseMethod.__init__(self, Post, session)

    def delete_old(self) -> int:
        lifetime = engine_config['lifetimes']['post']
        old = [x for x in
               self.get(False).filter(Post.added_date + timedelta(days=lifetime) <= datetime.now())]
        to_delete = len(old)
        self.delete_range(old)

        return to_delete
