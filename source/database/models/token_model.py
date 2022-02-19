from sqlalchemy import Column, String, BigInteger, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from pytz import timezone

from .. import Base
from .base_model import BaseModel
from .user_model import User


class Token(Base, BaseModel):
    __tablename__ = 'tokens'

    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String, nullable=False)
    user_id = Column(BigInteger, ForeignKey(User.id))
    added_date = Column(DateTime, nullable=False, default=datetime.now(timezone('Europe/Moscow')))

    def __init__(self, content: str, user_id: int):
        self.content = content
        self.user_id = user_id
        self.added_date = datetime.now(timezone('Europe/Moscow'))

    def __repr__(self):
        return f"<Token(user_id={self.user_id}, added={self.added_date.strftime('%D %T')})>"