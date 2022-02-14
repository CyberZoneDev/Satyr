from .base_methods import BaseMethod
from .. import Session
from ..models import Like


class LikeMethods(BaseMethod):
    def __init__(self, session=Session()):
        BaseMethod.__init__(self, Like, session)
