from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.level import UserLevelResponse, ExperienceLogResponse, LevelInfoResponse
from app.services.level_service import LevelService
from app.middleware.auth_middleware import get_current_user

router = APIRouter()


@router.get("/", response_model=list[UserLevelResponse])
async def list_levels(db: Session = Depends(get_db)):
    """获取所有等级配置"""
    return LevelService.get_level_configs(db)


@router.get("/my", response_model=LevelInfoResponse)
async def get_my_level(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取当前用户等级信息"""
    return LevelService.get_user_level_info(db, current_user)


@router.get("/experience-logs")
async def list_experience_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取经验值记录"""
    from app.models.level import ExperienceLog
    query = db.query(ExperienceLog).filter(ExperienceLog.user_id == current_user.id)
    total = query.count()
    items = query.order_by(ExperienceLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.get("/leaderboard")
async def get_leaderboard(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取等级排行榜"""
    from app.models.user import User
    users = (
        db.query(User)
        .filter(User.status == 1)
        .order_by(User.experience.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "rank": i + 1,
            "user_id": u.id,
            "nickname": u.nickname,
            "avatar_url": u.avatar_url,
            "level": u.level,
            "experience": u.experience,
        }
        for i, u in enumerate(users)
    ]
