from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.models.herb import Herb, HerbAttribute, HerbAttributeValue, HerbImage


class HerbService:
    @staticmethod
    def list_herbs(
        db: Session,
        search: Optional[str] = None,
        category: Optional[str] = None,
        attribute: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[List[Herb], int]:
        query = db.query(Herb).filter(Herb.is_system == 1)

        if search:
            query = query.filter(
                or_(
                    Herb.name.contains(search),
                    Herb.efficacy.contains(search),
                )
            )

        if category:
            query = query.filter(Herb.category == category)

        if attribute:
            query = query.join(HerbAttributeValue).join(HerbAttribute).filter(
                HerbAttribute.name == attribute
            )

        total = query.count()
        herbs = query.offset((page - 1) * page_size).limit(page_size).all()
        return herbs, total

    @staticmethod
    def get_herb(db: Session, herb_id: int) -> Optional[Herb]:
        return db.query(Herb).filter(Herb.id == herb_id).first()

    @staticmethod
    def create_herb(db: Session, **kwargs) -> Herb:
        herb = Herb(**kwargs)
        db.add(herb)
        db.commit()
        db.refresh(herb)
        return herb

    @staticmethod
    def update_herb(db: Session, herb_id: int, **kwargs) -> Optional[Herb]:
        herb = db.query(Herb).filter(Herb.id == herb_id).first()
        if not herb:
            return None
        for key, value in kwargs.items():
            setattr(herb, key, value)
        db.commit()
        db.refresh(herb)
        return herb

    @staticmethod
    def delete_herb(db: Session, herb_id: int) -> bool:
        herb = db.query(Herb).filter(Herb.id == herb_id).first()
        if not herb:
            return False
        db.delete(herb)
        db.commit()
        return True

    @staticmethod
    def list_attributes(db: Session) -> List[HerbAttribute]:
        return db.query(HerbAttribute).all()
