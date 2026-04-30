from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.schemas.user import AdminUserCreate, UserListItem, UserRoleUpdate, UserStatusUpdate, UserResponse
from app.middleware.auth_middleware import get_current_admin
from app.services.auth_service import AuthService

router = APIRouter()


@router.get("/users", response_model=list[UserListItem])
async def list_users(
    role: Optional[str] = None,
    status: Optional[int] = None,
    keyword: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """管理员查看用户列表（支持筛选和分页）"""
    query = db.query(User)

    if role:
        query = query.filter(User.role == role)
    if status is not None:
        query = query.filter(User.status == status)
    if keyword:
        query = query.filter(
            (User.phone.contains(keyword))
            | (User.nickname.contains(keyword))
            | (User.real_name.contains(keyword))
        )

    total = query.count()
    users = query.offset((page - 1) * page_size).limit(page_size).all()
    return users


@router.post("/users", response_model=UserResponse)
async def create_user(
    data: AdminUserCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """管理员创建用户（可指定角色）"""
    # 检查手机号是否已存在
    existing = db.query(User).filter(User.phone == data.phone).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该手机号已被注册",
        )

    # 校验角色合法性
    if data.role not in ("admin", "user"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="角色只能是 admin 或 user",
        )

    user = AuthService.create_user_by_admin(
        db,
        phone=data.phone,
        nickname=data.nickname,
        role=data.role,
        password=data.password,
    )
    return user


@router.put("/users/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: int,
    data: UserRoleUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """管理员修改用户角色"""
    if data.role not in ("admin", "user"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="角色只能是 admin 或 user",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )

    user.role = data.role
    db.commit()
    db.refresh(user)
    return user


@router.put("/users/{user_id}/status", response_model=UserResponse)
async def update_user_status(
    user_id: int,
    data: UserStatusUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """管理员禁用/启用用户（status: 1=正常, 0=禁用）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )

    # 禁止禁用最后一个管理员
    if user.role == "admin" and data.status == 0:
        admin_count = db.query(User).filter(User.role == "admin", User.status == 1).count()
        if admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="不能禁用最后一个管理员",
            )

    user.status = data.status
    db.commit()
    db.refresh(user)
    return user


