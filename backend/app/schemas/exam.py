from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.schemas.question import AnswerResult


class ExamGenerateRequest(BaseModel):
    count: int = 10
    type: Optional[str] = None
    difficulty: Optional[str] = None


class ExamStartRequest(BaseModel):
    question_ids: List[int]
    exam_name: Optional[str] = None


class ExamSubmitRequest(BaseModel):
    answers: List[dict]  # [{question_id, answers: [], time_spent}]


class ExamResultResponse(BaseModel):
    id: int
    user_id: int
    exam_name: Optional[str] = None
    total_questions: int
    correct_count: int
    score: float
    max_score: float
    time_spent: Optional[int] = None
    completed_at: datetime

    class Config:
        from_attributes = True


class WrongAnswerResponse(BaseModel):
    id: int
    user_id: int
    question_id: int
    user_answers: Optional[List[str]] = None
    correct_answers: Optional[List[str]] = None
    wrong_count: int = 1
    is_mastered: int = 0
    last_wrong_at: datetime
    mastered_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
