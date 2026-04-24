from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserLevelBase(BaseModel):
    level: int
    name: str
    icon: Optional[str] = None
    min_experience: int
    max_experience: int
    color: Optional[str] = None
    privileges: Optional[str] = None


class UserLevelResponse(UserLevelBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ExperienceLogResponse(BaseModel):
    id: int
    user_id: int
    type: str
    description: Optional[str] = None
    experience: int
    balance: int
    related_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class LevelInfoResponse(BaseModel):
    level: int
    experience: int
    level_name: str
    level_color: str
    next_level_exp: Optional[int] = None
    level_progress: float
    total_score: int
    streak_days: int
