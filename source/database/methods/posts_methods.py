from .base_methods import BaseMethod
from .. import Session
from ..models import Post


class PostMethods(BaseMethod):
    def __init__(self, session=Session()):
        BaseMethod.__init__(self, Post, session)
