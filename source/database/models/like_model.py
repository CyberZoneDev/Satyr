from sqlalchemy import Column, BigInteger, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from pytz import timezone

from .. import Base
from .base_model import BaseModel
from .user_model import User
from .post_model import Post


class Like(Base, BaseModel):
    __tablename__ = 'likes'

    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(BigInteger, ForeignKey(Post.id, ondelete='CASCADE'))
    user_id = Column(BigInteger, ForeignKey(User.id, ondelete='CASCADE'))
    added_date = Column(DateTime, nullable=False, default=datetime.now(timezone('Europe/Moscow')))

    def __init__(self, post_id: int, user_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post_id = post_id
        self.user_id = user_id
        self.added_date = datetime.now(timezone('Europe/Moscow'))

    def __repr__(self):
        return f"<Like(user_id={self.user_id}, post_id={self.post_id}, added={self.added_date.strftime('%D %T')})>"

