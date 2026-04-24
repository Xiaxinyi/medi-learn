from sqlalchemy import Column, BigInteger, String, Enum, Text, Date, DateTime, Integer, SmallInteger
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    wechat_openid = Column(String(100), index=True, nullable=True)
    wechat_unionid = Column(String(100), nullable=True)
    nickname = Column(String(50), nullable=True)
    real_name = Column(String(50), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    email = Column(String(100), index=True, nullable=True)
    gender = Column(Enum('male', 'female', 'other'), default='other')
    birthday = Column(Date, nullable=True)
    bio = Column(Text, nullable=True)
    password_hash = Column(String(255), nullable=True)
    role = Column(Enum('admin', 'user'), default='user', index=True)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    total_score = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    last_study_date = Column(Date, nullable=True)
    status = Column(SmallInteger, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
