import random
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.jwt_utils import create_access_token, get_password_hash, verify_password


class AuthService:
    # 模拟验证码存储（生产环境应使用Redis）
    _code_store: dict = {}

    @classmethod
    def send_verification_code(cls, phone: str) -> str:
        """发送验证码（模拟）"""
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        cls._code_store[phone] = {
            "code": code,
            "expires_at": datetime.now() + timedelta(minutes=5),
        }
        print(f"验证码已发送: {phone} -> {code}")
        return code

    @classmethod
    def verify_code(cls, phone: str, code: str) -> bool:
        """验证验证码"""
        record = cls._code_store.get(phone)
        if not record:
            return False
        if datetime.now() > record["expires_at"]:
            return False
        return record["code"] == code

    @classmethod
    def get_or_create_user_by_phone(cls, db: Session, phone: str) -> User:
        """根据手机号获取或创建用户"""
        user = db.query(User).filter(User.phone == phone).first()
        if not user:
            user = User(phone=phone, nickname=f"用户{phone[-4:]}")
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    @classmethod
    def create_token_for_user(cls, user: User) -> str:
        """为用户创建访问令牌"""
        return create_access_token(data={"sub": str(user.id)})

    @classmethod
    def get_user_by_wechat(cls, db: Session, openid: str) -> Optional[User]:
        """根据微信openid获取用户"""
        return db.query(User).filter(User.wechat_openid == openid).first()

    @classmethod
    def create_user_by_wechat(cls, db: Session, openid: str, unionid: Optional[str] = None) -> User:
        """通过微信信息创建用户"""
        user = User(
            wechat_openid=openid,
            wechat_unionid=unionid,
            nickname="微信用户",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
