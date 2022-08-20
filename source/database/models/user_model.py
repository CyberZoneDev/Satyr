from sqlalchemy import Column, BigInteger, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone

from .. import Base
from .base_model import BaseModel


class User(Base, BaseModel):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    added_date = Column(DateTime, nullable=False, default=datetime.now(timezone('Europe/Moscow')))

    likes = relationship('Like', uselist=True)
    token = relationship('Token', uselist=False)

    def __init__(self, id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.added_date = datetime.now(timezone('Europe/Moscow'))

    def __repr__(self):
        return f"<User(id={self.id}, added={self.added_date.strftime('%D %T')})>"
