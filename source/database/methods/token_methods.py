from .base_methods import BaseMethod
from .. import Session
from ..models import Token


class TokenMethods(BaseMethod):
    def __init__(self, session=Session()):
        BaseMethod.__init__(self, Token, session)
