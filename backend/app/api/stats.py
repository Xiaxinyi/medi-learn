from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.exam import ExamResult, AnswerRecord
from app.models.level import ExperienceLog

router = APIRouter()


@router.get("/overview")
async def get_overview(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取学习概览"""
    total_answered = db.query(AnswerRecord).filter(AnswerRecord.user_id == current_user.id).count()
    correct_count = db.query(AnswerRecord).filter(
        AnswerRecord.user_id == current_user.id,
        AnswerRecord.is_correct == 1,
    ).count()
    exam_count = db.query(ExamResult).filter(ExamResult.user_id == current_user.id).count()

    return {
        "total_answered": total_answered,
        "correct_count": correct_count,
        "accuracy_rate": round(correct_count / total_answered * 100, 2) if total_answered > 0 else 0,
        "exam_count": exam_count,
        "level": current_user.level,
        "experience": current_user.experience,
        "streak_days": current_user.streak_days,
    }


@router.get("/daily")
async def get_daily_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取每日学习统计"""
    today = datetime.now().date()
    today_count = db.query(AnswerRecord).filter(
        AnswerRecord.user_id == current_user.id,
        func.date(AnswerRecord.answered_at) == today,
    ).count()

    today_correct = db.query(AnswerRecord).filter(
        AnswerRecord.user_id == current_user.id,
        AnswerRecord.is_correct == 1,
        func.date(AnswerRecord.answered_at) == today,
    ).count()

    return {
        "date": str(today),
        "answered": today_count,
        "correct": today_correct,
        "accuracy": round(today_correct / today_count * 100, 2) if today_count > 0 else 0,
    }


@router.get("/trend")
async def get_trend(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取学习趋势"""
    dates = []
    for i in range(days - 1, -1, -1):
        date = (datetime.now() - timedelta(days=i)).date()
        count = db.query(AnswerRecord).filter(
            AnswerRecord.user_id == current_user.id,
            func.date(AnswerRecord.answered_at) == date,
        ).count()
        correct = db.query(AnswerRecord).filter(
            AnswerRecord.user_id == current_user.id,
            AnswerRecord.is_correct == 1,
            func.date(AnswerRecord.answered_at) == date,
        ).count()
        dates.append({
            "date": str(date),
            "answered": count,
            "correct": correct,
        })
    return dates


@router.get("/accuracy")
async def get_accuracy(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取各题型正确率"""
    from app.models.question import Question
    single_total = db.query(AnswerRecord).join(Question).filter(
        AnswerRecord.user_id == current_user.id,
        Question.type == "single",
    ).count()
    single_correct = db.query(AnswerRecord).join(Question).filter(
        AnswerRecord.user_id == current_user.id,
        Question.type == "single",
        AnswerRecord.is_correct == 1,
    ).count()

    multiple_total = db.query(AnswerRecord).join(Question).filter(
        AnswerRecord.user_id == current_user.id,
        Question.type == "multiple",
    ).count()
    multiple_correct = db.query(AnswerRecord).join(Question).filter(
        AnswerRecord.user_id == current_user.id,
        Question.type == "multiple",
        AnswerRecord.is_correct == 1,
    ).count()

    return {
        "single": {
            "total": single_total,
            "correct": single_correct,
            "rate": round(single_correct / single_total * 100, 2) if single_total > 0 else 0,
        },
        "multiple": {
            "total": multiple_total,
            "correct": multiple_correct,
            "rate": round(multiple_correct / multiple_total * 100, 2) if multiple_total > 0 else 0,
        },
    }
