from sqlalchemy import Column, BigInteger, String, Text, Integer, SmallInteger, DateTime, ForeignKey, JSON, DECIMAL
from sqlalchemy.sql import func
from app.database import Base


class AnswerRecord(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "answer_records"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    user_answers = Column(JSON, nullable=True)
    is_correct = Column(SmallInteger, nullable=True)
    score = Column(DECIMAL(5, 2), nullable=True)
    time_spent = Column(Integer, nullable=True)
    answered_at = Column(DateTime, server_default=func.now(), index=True)


class ExamResult(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "exam_results"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    exam_name = Column(String(100), nullable=True)
    total_questions = Column(Integer, nullable=True)
    correct_count = Column(Integer, nullable=True)
    score = Column(DECIMAL(5, 2), nullable=True)
    max_score = Column(DECIMAL(5, 2), nullable=True)
    time_spent = Column(Integer, nullable=True)
    completed_at = Column(DateTime, server_default=func.now(), index=True)


class WrongAnswer(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "wrong_answers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_answers = Column(JSON, nullable=True)
    correct_answers = Column(JSON, nullable=True)
    wrong_count = Column(Integer, default=1)
    last_wrong_at = Column(DateTime, server_default=func.now())
    is_mastered = Column(SmallInteger, default=0)
    mastered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
