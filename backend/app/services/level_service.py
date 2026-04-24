from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.level import UserLevel, ExperienceLog


class LevelService:
    # 经验值获取规则
    EXP_RULES = {
        "login": 10,
        "study_herb": 5,
        "answer_correct": 10,
        "answer_wrong": 2,
        "exam_complete": 50,
        "favorite": 3,
        "note": 5,
        "wrongbook_review": 8,
        "streak_week": 50,
        "streak_month": 200,
        "feedback_adopted": 30,
    }

    @staticmethod
    def get_level_configs(db: Session) -> list:
        return db.query(UserLevel).order_by(UserLevel.level).all()

    @staticmethod
    def get_user_level_info(db: Session, user: User) -> dict:
        current_level = (
            db.query(UserLevel).filter(UserLevel.level == user.level).first()
        )
        next_level = (
            db.query(UserLevel).filter(UserLevel.level == user.level + 1).first()
        )

        progress = 0.0
        if current_level and next_level:
            range_exp = next_level.min_experience - current_level.min_experience
            current_exp = user.experience - current_level.min_experience
            progress = (current_exp / range_exp) * 100 if range_exp > 0 else 100

        return {
            "level": user.level,
            "experience": user.experience,
            "level_name": current_level.name if current_level else "",
            "level_color": current_level.color if current_level else "#999",
            "next_level_exp": next_level.min_experience if next_level else None,
            "level_progress": min(progress, 100),
            "total_score": user.total_score,
            "streak_days": user.streak_days,
        }

    @classmethod
    def add_experience(
        cls, db: Session, user: User, exp_type: str, description: str = "", related_id: Optional[str] = None
    ) -> int:
        exp = cls.EXP_RULES.get(exp_type, 0)
        if exp <= 0:
            return 0

        user.experience += exp

        # 检查升级
        next_level = (
            db.query(UserLevel)
            .filter(UserLevel.min_experience <= user.experience)
            .filter(UserLevel.level > user.level)
            .order_by(UserLevel.level)
            .first()
        )
        if next_level:
            user.level = next_level.level

        # 记录经验日志
        log = ExperienceLog(
            user_id=user.id,
            type=exp_type,
            description=description,
            experience=exp,
            balance=user.experience,
            related_id=related_id,
        )
        db.add(log)
        db.commit()

        return exp
