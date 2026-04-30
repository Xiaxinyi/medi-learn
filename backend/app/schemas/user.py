from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


class UserBase(BaseModel):
    nickname: Optional[str] = None
    real_name: Optional[str] = None
    avatar_url: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = 'other'
    birthday: Optional[date] = None
    bio: Optional[str] = None


class UserCreate(UserBase):
    phone: str
    password: Optional[str] = None
    wechat_openid: Optional[str] = None


class UserUpdate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    phone: Optional[str] = None
    role: str = 'user'
    level: int = 1
    experience: int = 0
    level_name: Optional[str] = None
    level_color: Optional[str] = None
    next_level_exp: Optional[int] = None
    level_progress: float = 0.0
    total_score: int = 0
    streak_days: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    phone: str
    code: str


class WechatLogin(BaseModel):
    code: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class PhoneCodeRequest(BaseModel):
    phone: str


class AdminUserCreate(BaseModel):
    phone: str
    nickname: str
    role: str = 'user'
    password: Optional[str] = None


class UserListItem(UserBase):
    id: int
    phone: Optional[str] = None
    role: str
    level: int = 1
    experience: int = 0
    status: int = 1
    created_at: datetime

    class Config:
        from_attributes = True


class UserRoleUpdate(BaseModel):
    role: str


class UserStatusUpdate(BaseModel):
    status: int
