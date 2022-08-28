from .base_methods import BaseMethod
from .. import Session
from ..models import User, Token
from datetime import datetime, timedelta
from core import engine_config


class UserMethods(BaseMethod):
    def __init__(self, session=Session()):
        BaseMethod.__init__(self, User, session)

    def delete_old(self) -> int:
        lifetime = engine_config['lifetimes']['user']
        old = [x for x in
               self.get(False)
               # .join(Token, User.id == Token.user_id, isouter=True)
               .filter(User.added_date + timedelta(days=lifetime) <= datetime.now())
               .filter_by(token=None)]
        to_delete = len(old)
        self.delete_range(old)

        return to_delete
