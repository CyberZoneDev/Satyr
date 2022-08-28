from typing import Optional

from .base_methods import BaseMethod
from .. import Session
from ..models import Token
from source.utils import Aes
from core import S_T_K


class TokenMethods(BaseMethod):
    def __init__(self, session=Session()):
        BaseMethod.__init__(self, Token, session)

    def add(self, c_object: Token, **kwargs) -> Optional[Token]:
        if not isinstance(c_object, self.type):
            raise TypeError(f'Invalid type. Wanted: {self.type}, Got: {c_object.__class__}')

        if isinstance(c_object.content, str):
            c_object.content = Aes.encrypt(c_object.content, S_T_K)

        try:
            self.session.add(c_object)
            self.session.commit()
        except:
            self.session.rollback()
            return None

        return c_object

    def get(self, **kwargs) -> list:
        kwargs['dl'] = kwargs.get('dl') if kwargs.get('dl') else False
        result = [x for x in self.session.query(self.type).filter_by(**kwargs)]
        return result

    def disable(self, c_object: Token) -> None:
        if not isinstance(c_object, self.type):
            raise TypeError(f'Invalid type. Wanted: {self.type}, Got: {c_object.__class__}')

        c_object.dl = True

        try:
            self.session.commit()
        except:
            self.session.rollback()

    def update(self, c_object: Token) -> Optional[Token]:
        if not isinstance(c_object, self.type):
            raise TypeError(f'Invalid type. Wanted: {self.type}, Got: {c_object.__class__}')

        if isinstance(c_object.content, str):
            c_object.content = Aes.encrypt(c_object.content, S_T_K)

        try:
            self.session.commit()
            return c_object
        except:
            self.session.rollback()
            return None
