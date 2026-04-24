from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.user import UserLogin, WechatLogin, TokenResponse, PhoneCodeRequest, UserResponse, UserUpdate
from app.services.auth_service import AuthService
from app.middleware.auth_middleware import get_current_user
from app.utils.jwt_utils import create_access_token, decode_access_token

router = APIRouter()


@router.post("/send-code")
async def send_verification_code(request: PhoneCodeRequest, db: Session = Depends(get_db)):
    """发送短信验证码（模拟，直接返回验证码）"""
    code = AuthService.send_verification_code(request.phone)
    return {"message": "验证码已发送", "phone": request.phone, "code": code}


@router.post("/login-phone", response_model=TokenResponse)
async def login_with_phone(login_data: UserLogin, db: Session = Depends(get_db)):
    """手机号验证码登录"""
    if not AuthService.verify_code(login_data.phone, login_data.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码错误或已过期",
        )

    user = AuthService.get_or_create_user_by_phone(db, login_data.phone)
    access_token = AuthService.create_token_for_user(user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 60 * 60 * 24 * 7,
        "user": user,
    }


@router.post("/login-wechat", response_model=TokenResponse)
async def login_with_wechat(login_data: WechatLogin, db: Session = Depends(get_db)):
    """微信授权登录（模拟，code直接作为openid）"""
    openid = login_data.code  # 实际应调用微信接口换取openid
    user = AuthService.get_user_by_wechat(db, openid)
    if not user:
        user = AuthService.create_user_by_wechat(db, openid)

    access_token = AuthService.create_token_for_user(user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 60 * 60 * 24 * 7,
        "user": user,
    }


@router.post("/bind-phone")
async def bind_phone(phone: str, code: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """绑定手机号"""
    if not AuthService.verify_code(phone, code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码错误或已过期",
        )
    existing = db.query(type(current_user)).filter_by(phone=phone).first()
    if existing and existing.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该手机号已被绑定",
        )
    current_user.phone = phone
    db.commit()
    return {"message": "绑定成功"}


@router.post("/refresh-token")
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """刷新Token"""
    payload = decode_access_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌无效或已过期",
        )
    from app.models.user import User
    user = db.query(User).filter(User.id == int(payload.get("sub"))).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
        )
    access_token = AuthService.create_token_for_user(user)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 60 * 60 * 24 * 7,
        "user": user,
    }


@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user = Depends(get_current_user)):
    """获取用户信息"""
    return current_user


@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """更新用户信息"""
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user
