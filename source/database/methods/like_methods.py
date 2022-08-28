from .base_methods import BaseMethod
from .. import Session
from ..models import Like
from datetime import datetime, timedelta
from core import engine_config


class LikeMethods(BaseMethod):
    def __init__(self, session=Session()):
        BaseMethod.__init__(self, Like, session)

    def delete(self, c_object: Like) -> bool:
        return super().delete(c_object)

    def delete_old(self) -> int:
        lifetime = engine_config['lifetimes']['like']
        old = [x for x in
               self.get(False).filter(Like.added_date + timedelta(days=lifetime) <= datetime.now())]
        to_delete = len(old)
        self.delete_range(old)

        return to_delete
