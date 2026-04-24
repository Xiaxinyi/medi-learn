from sqlalchemy import Column, BigInteger, String, Text, Enum, SmallInteger, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Question(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    type = Column(Enum('single', 'multiple'), nullable=False)
    content = Column(Text, nullable=False)
    difficulty = Column(Enum('easy', 'medium', 'hard'), default='medium')
    explanation = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)
    herb_ids = Column(JSON, nullable=True)
    is_system = Column(SmallInteger, default=1)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    options = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan")


class QuestionOption(Base):
    __table_args__ = {"sqlite_autoincrement": True}
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    option_key = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)
    is_correct = Column(SmallInteger, default=0)
    sort_order = Column(Integer, default=0)

    question = relationship("Question", back_populates="options")
