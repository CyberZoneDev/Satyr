from typing import Optional

from sqlalchemy import Column, String, BigInteger, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from pytz import timezone

from .. import Base
from .base_model import BaseModel
from .user_model import User
from source.utils import Aes
from os import environ


class Token(Base, BaseModel):
    __tablename__ = 'tokens'

    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String, nullable=False)
    user_id = Column(BigInteger, ForeignKey(User.id))
    added_date = Column(DateTime, nullable=False, default=datetime.now(timezone('Europe/Moscow')))
    dl = Column(Boolean, nullable=False, default=False)

    def __init__(self, content: str, user_id: int):
        self.content = content
        self.user_id = user_id
        self.added_date = datetime.now(timezone('Europe/Moscow'))

    def get_decoded_content(self) -> Optional[str]:
        if self.content:
            return Aes.decrypt(self.content, environ['S_T_K'])
        else:
            return None

    def __repr__(self):
        return f"<Token(user_id={self.user_id}, added={self.added_date.strftime('%D %T')}, dl={self.dl})>"