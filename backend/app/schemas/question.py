from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class QuestionOptionBase(BaseModel):
    option_key: str
    content: str
    is_correct: bool = False
    sort_order: int = 0


class QuestionOptionCreate(QuestionOptionBase):
    pass


class QuestionOptionResponse(QuestionOptionBase):
    id: int
    question_id: int

    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    type: str  # single, multiple
    content: str
    difficulty: str = "medium"  # easy, medium, hard
    explanation: Optional[str] = None
    tags: Optional[List[str]] = None
    herb_ids: Optional[List[int]] = None


class QuestionCreate(QuestionBase):
    options: List[QuestionOptionCreate]


class QuestionUpdate(BaseModel):
    type: Optional[str] = None
    content: Optional[str] = None
    difficulty: Optional[str] = None
    explanation: Optional[str] = None
    tags: Optional[List[str]] = None
    herb_ids: Optional[List[int]] = None
    options: Optional[List[QuestionOptionCreate]] = None


class QuestionResponse(QuestionBase):
    id: int
    is_system: int = 1
    created_at: datetime
    updated_at: datetime
    options: List[QuestionOptionResponse] = []

    class Config:
        from_attributes = True


class QuestionListResponse(BaseModel):
    id: int
    type: str
    content: str
    difficulty: str
    tags: Optional[List[str]] = None
    is_system: int = 1
    created_at: datetime

    class Config:
        from_attributes = True


class AnswerSubmit(BaseModel):
    question_id: int
    answers: List[str]
    time_spent: Optional[int] = None  # 秒


class AnswerResult(BaseModel):
    question_id: int
    is_correct: bool
    score: float
    correct_answers: List[str]
    user_answers: List[str]
    explanation: Optional[str] = None
