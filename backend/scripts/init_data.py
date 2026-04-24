#!/usr/bin/env python3
"""数据库初始化脚本：创建等级配置、属性标签等基础数据"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.level import UserLevel
from app.models.herb import HerbAttribute
from app.models.user import User
from app.utils.jwt_utils import get_password_hash


def init_levels(db):
    """初始化等级配置"""
    levels = [
        {"level": 1, "name": "初学弟子", "min_experience": 0, "max_experience": 99, "color": "#8B4513", "privileges": "基础学习"},
        {"level": 2, "name": "采药童子", "min_experience": 100, "max_experience": 299, "color": "#228B22", "privileges": "可收藏草药"},
        {"level": 3, "name": "识草学徒", "min_experience": 300, "max_experience": 599, "color": "#32CD32", "privileges": "可添加笔记"},
        {"level": 4, "name": "辨药小生", "min_experience": 600, "max_experience": 999, "color": "#4169E1", "privileges": "解锁每日挑战"},
        {"level": 5, "name": "方剂学徒", "min_experience": 1000, "max_experience": 1499, "color": "#6495ED", "privileges": "方剂学习"},
        {"level": 6, "name": "岐黄学子", "min_experience": 1500, "max_experience": 2199, "color": "#9370DB", "privileges": "错题重练"},
        {"level": 7, "name": "本草达人", "min_experience": 2200, "max_experience": 3099, "color": "#BA55D3", "privileges": "排行榜展示"},
        {"level": 8, "name": "杏林新秀", "min_experience": 3100, "max_experience": 4299, "color": "#FF6347", "privileges": "高级试题"},
        {"level": 9, "name": "国医传人", "min_experience": 4300, "max_experience": 5999, "color": "#FF4500", "privileges": "专家论坛"},
        {"level": 10, "name": "岐黄圣手", "min_experience": 6000, "max_experience": 99999, "color": "#FFD700", "privileges": "全功能解锁"},
    ]

    for data in levels:
        existing = db.query(UserLevel).filter(UserLevel.level == data["level"]).first()
        if not existing:
            db.add(UserLevel(**data))
    db.commit()
    print(f"已初始化 {len(levels)} 个等级配置")


def init_herb_attributes(db):
    """初始化草药属性标签"""
    attributes = [
        # 性味
        {"name": "寒", "group_name": "性味", "color": "#4169E1"},
        {"name": "热", "group_name": "性味", "color": "#FF4500"},
        {"name": "温", "group_name": "性味", "color": "#FF8C00"},
        {"name": "凉", "group_name": "性味", "color": "#87CEEB"},
        {"name": "平", "group_name": "性味", "color": "#90EE90"},
        {"name": "甘", "group_name": "性味", "color": "#FFD700"},
        {"name": "苦", "group_name": "性味", "color": "#8B4513"},
        {"name": "辛", "group_name": "性味", "color": "#FF6347"},
        {"name": "咸", "group_name": "性味", "color": "#708090"},
        {"name": "酸", "group_name": "性味", "color": "#DC143C"},
        # 归经
        {"name": "心", "group_name": "归经", "color": "#DC143C"},
        {"name": "肝", "group_name": "归经", "color": "#228B22"},
        {"name": "脾", "group_name": "归经", "color": "#FFD700"},
        {"name": "肺", "group_name": "归经", "color": "#FFFFFF"},
        {"name": "肾", "group_name": "归经", "color": "#4169E1"},
        {"name": "胃", "group_name": "归经", "color": "#F4A460"},
        {"name": "胆", "group_name": "归经", "color": "#32CD32"},
        {"name": "大肠", "group_name": "归经", "color": "#8B4513"},
        {"name": "小肠", "group_name": "归经", "color": "#FF6347"},
        {"name": "膀胱", "group_name": "归经", "color": "#87CEEB"},
        {"name": "三焦", "group_name": "归经", "color": "#9370DB"},
        {"name": "心包", "group_name": "归经", "color": "#DC143C"},
        # 功效分类
        {"name": "解表", "group_name": "功效", "color": "#87CEFA"},
        {"name": "清热", "group_name": "功效", "color": "#4169E1"},
        {"name": "泻下", "group_name": "功效", "color": "#8B4513"},
        {"name": "祛湿", "group_name": "功效", "color": "#228B22"},
        {"name": "温里", "group_name": "功效", "color": "#FF4500"},
        {"name": "理气", "group_name": "功效", "color": "#FFD700"},
        {"name": "活血化瘀", "group_name": "功效", "color": "#DC143C"},
        {"name": "止血", "group_name": "功效", "color": "#8B0000"},
        {"name": "补益", "group_name": "功效", "color": "#FF8C00"},
        {"name": "安神", "group_name": "功效", "color": "#9370DB"},
        {"name": "平肝息风", "group_name": "功效", "color": "#4682B4"},
        {"name": "收涩", "group_name": "功效", "color": "#A0522D"},
    ]

    for data in attributes:
        existing = db.query(HerbAttribute).filter(HerbAttribute.name == data["name"]).first()
        if not existing:
            db.add(HerbAttribute(**data))
    db.commit()
    print(f"已初始化 {len(attributes)} 个属性标签")


def init_admin_user(db):
    """初始化管理员用户"""
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        admin = User(
            phone="admin",
            nickname="管理员",
            role="admin",
            status=1,
        )
        db.add(admin)
        db.commit()
        print("已创建管理员用户")


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        init_levels(db)
        init_herb_attributes(db)
        init_admin_user(db)
        print("数据库初始化完成")
    finally:
        db.close()


if __name__ == "__main__":
    main()
