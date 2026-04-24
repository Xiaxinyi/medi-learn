from sqlalchemy import Column, BigInteger, Integer, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class LearningStat(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "learning_stats"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    stat_date = Column(Date, nullable=False)
    study_duration = Column(Integer, default=0)
    herbs_viewed = Column(Integer, default=0)
    questions_answered = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
