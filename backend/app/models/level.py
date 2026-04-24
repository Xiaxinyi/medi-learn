from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class UserLevel(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "user_levels"

    id = Column(Integer, primary_key=True)
    level = Column(Integer, nullable=False, unique=True, index=True)
    name = Column(String(50), nullable=False)
    icon = Column(String(255), nullable=True)
    min_experience = Column(Integer, nullable=False)
    max_experience = Column(Integer, nullable=False)
    color = Column(String(20), nullable=True)
    privileges = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class ExperienceLog(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "experience_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)
    description = Column(String(200), nullable=True)
    experience = Column(Integer, nullable=False)
    balance = Column(Integer, nullable=False)
    related_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), index=True)
