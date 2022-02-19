from sqlalchemy import Column, BigInteger, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone

from .. import Base
from .base_model import BaseModel


class Group(Base, BaseModel):
    __tablename__ = 'groups'

    id = Column(BigInteger, primary_key=True)
    added_date = Column(DateTime, nullable=False, default=datetime.now(timezone('Europe/Moscow')))

    posts = relationship('Post', uselist=True)

    def __init__(self, id: int):
        self.id = id
        self.added_date = datetime.now(timezone('Europe/Moscow'))

    def __repr__(self):
        return f"<Group(id={self.id}, added={self.added_date.strftime('%D %T')})>"