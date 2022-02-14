from .base_methods import BaseMethod
from .. import Session
from ..models import User


class UserMethods(BaseMethod):
    def __init__(self, session=Session()):
        BaseMethod.__init__(self, User, session)
