from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
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
        query = db.query(Herb).filter(Herb.is_system == 1).options(
            joinedload(Herb.images),
            joinedload(Herb.attribute_values).joinedload(HerbAttributeValue.attribute),
        )

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
        attribute_ids = kwargs.pop("attribute_ids", None)
        image_urls = kwargs.pop("image_urls", None)

        kwargs.setdefault("is_system", 1)
        herb = Herb(**kwargs)
        db.add(herb)
        db.commit()
        db.refresh(herb)

        if attribute_ids:
            for attr_id in attribute_ids:
                attr_value = HerbAttributeValue(herb_id=herb.id, attribute_id=attr_id)
                db.add(attr_value)

        if image_urls:
            for idx, url in enumerate(image_urls):
                image = HerbImage(
                    herb_id=herb.id,
                    image_url=url,
                    sort_order=idx,
                    is_cover=1 if idx == 0 else 0
                )
                db.add(image)

        if attribute_ids or image_urls:
            db.commit()
            db.refresh(herb)

        return herb

    @staticmethod
    def update_herb(db: Session, herb_id: int, **kwargs) -> Optional[Herb]:
        herb = db.query(Herb).filter(Herb.id == herb_id).first()
        if not herb:
            return None

        attribute_ids = kwargs.pop("attribute_ids", None)

        for key, value in kwargs.items():
            setattr(herb, key, value)

        if attribute_ids is not None:
            db.query(HerbAttributeValue).filter(HerbAttributeValue.herb_id == herb_id).delete()
            for attr_id in attribute_ids:
                attr_value = HerbAttributeValue(herb_id=herb.id, attribute_id=attr_id)
                db.add(attr_value)

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
