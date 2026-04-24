from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.formula import Formula, FormulaHerb


class FormulaService:
    @staticmethod
    def list_formulas(
        db: Session,
        search: Optional[str] = None,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[List[Formula], int]:
        query = db.query(Formula).filter(Formula.is_system == 1)

        if search:
            query = query.filter(
                or_(
                    Formula.name.contains(search),
                    Formula.indications.contains(search),
                )
            )

        if category:
            query = query.filter(Formula.category == category)

        total = query.count()
        formulas = query.offset((page - 1) * page_size).limit(page_size).all()
        return formulas, total

    @staticmethod
    def get_formula(db: Session, formula_id: int) -> Optional[Formula]:
        return db.query(Formula).filter(Formula.id == formula_id).first()

    @staticmethod
    def get_formulas_by_herb(db: Session, herb_id: int) -> List[Formula]:
        return (
            db.query(Formula)
            .join(FormulaHerb)
            .filter(FormulaHerb.herb_id == herb_id)
            .all()
        )
