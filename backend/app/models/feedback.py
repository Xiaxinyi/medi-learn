from sqlalchemy import Column, Integer, BigInteger, String, Text, SmallInteger, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.sql import func
from app.database import Base


class Feedback(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(Enum('suggestion', 'bug', 'complaint', 'other'), default='suggestion', index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    contact = Column(String(100), nullable=True)
    images = Column(JSON, nullable=True)
    status = Column(Enum('pending', 'processing', 'resolved', 'rejected'), default='pending', index=True)
    admin_reply = Column(Text, nullable=True)
    replied_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
