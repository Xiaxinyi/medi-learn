from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate, FeedbackResponse
from app.middleware.auth_middleware import get_current_user, get_current_admin
from app.models.feedback import Feedback

router = APIRouter()


@router.post("/", response_model=FeedbackResponse)
async def create_feedback(
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """提交反馈"""
    feedback = Feedback(
        user_id=current_user.id,
        type=data.type,
        title=data.title,
        content=data.content,
        contact=data.contact,
        images=data.images,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


@router.get("/my")
async def list_my_feedback(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取我的反馈列表"""
    query = db.query(Feedback).filter(Feedback.user_id == current_user.id)
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.get("/")
async def list_all_feedback(
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """获取所有反馈列表（admin）"""
    query = db.query(Feedback)
    if status:
        query = query.filter(Feedback.status == status)
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.get("/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取反馈详情"""
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="反馈不存在")
    if feedback.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权查看")
    return feedback


@router.put("/{feedback_id}/reply", response_model=FeedbackResponse)
async def reply_feedback(
    feedback_id: int,
    reply: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """管理员回复"""
    from datetime import datetime
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="反馈不存在")
    feedback.admin_reply = reply
    feedback.replied_at = datetime.now()
    feedback.status = "resolved"
    db.commit()
    db.refresh(feedback)
    return feedback


@router.put("/{feedback_id}/status", response_model=FeedbackResponse)
async def update_feedback_status(
    feedback_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """更新反馈状态"""
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="反馈不存在")
    feedback.status = status
    db.commit()
    db.refresh(feedback)
    return feedback
