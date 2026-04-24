from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class FeedbackBase(BaseModel):
    type: str = "suggestion"  # suggestion, bug, complaint, other
    title: str
    content: str
    contact: Optional[str] = None
    images: Optional[List[str]] = None


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackUpdate(BaseModel):
    status: Optional[str] = None
    admin_reply: Optional[str] = None


class FeedbackResponse(FeedbackBase):
    id: int
    user_id: int
    status: str = "pending"
    admin_reply: Optional[str] = None
    replied_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
