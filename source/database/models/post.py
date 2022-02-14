from sqlalchemy import Column, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone

from .. import Base
from .base_model import BaseModel
from .group import Group


class Post(Base, BaseModel):
    __tablename__ = 'posts'

    id = Column(BigInteger, primary_key=True)
    group_id = Column(BigInteger, ForeignKey(Group.id))
    added_date = Column(DateTime, nullable=False, default=datetime.now(timezone('Europe/Moscow')))

    likes = relationship('Like', uselist=True)

    def __init__(self, id: int, group_id: int):
        self.id = id
        self.group_id = group_id
        self.added_date = datetime.now(timezone('Europe/Moscow'))

    def __repr__(self):
        return f"<Post(id={self.id}, group_id={self.group_id}, added={self.added_date.strftime('%D %T')})>"
