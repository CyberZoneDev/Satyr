from .base_methods import BaseMethod
from .. import Session
from ..models import Group


class GroupMethods(BaseMethod):
    def __init__(self, session=Session()):
        BaseMethod.__init__(self, Group, session)
