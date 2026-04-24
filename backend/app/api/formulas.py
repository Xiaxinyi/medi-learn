from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.formula import FormulaCreate, FormulaUpdate, FormulaResponse
from app.services.formula_service import FormulaService
from app.middleware.auth_middleware import get_current_admin

router = APIRouter()


@router.get("/")
async def list_formulas(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取方剂列表"""
    formulas, total = FormulaService.list_formulas(db, search, category, page, page_size)
    return {
        "items": formulas,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/{formula_id}", response_model=FormulaResponse)
async def get_formula(formula_id: int, db: Session = Depends(get_db)):
    """获取方剂详情"""
    formula = FormulaService.get_formula(db, formula_id)
    if not formula:
        raise HTTPException(status_code=404, detail="方剂不存在")
    return formula


@router.post("/", response_model=FormulaResponse)
async def create_formula(
    data: FormulaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """添加方剂（admin）"""
    from app.models.formula import Formula, FormulaHerb
    formula = Formula(
        name=data.name,
        source=data.source,
        category=data.category,
        indications=data.indications,
        usage=data.usage,
        modifications=data.modifications,
        precautions=data.precautions,
    )
    db.add(formula)
    db.commit()
    db.refresh(formula)

    for herb in data.herbs:
        fh = FormulaHerb(
            formula_id=formula.id,
            herb_id=herb.herb_id,
            herb_name=herb.herb_name,
            dosage=herb.dosage,
            role=herb.role,
            sort_order=herb.sort_order,
        )
        db.add(fh)
    db.commit()
    db.refresh(formula)
    return formula


@router.put("/{formula_id}", response_model=FormulaResponse)
async def update_formula(
    formula_id: int,
    data: FormulaUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """更新方剂（admin）"""
    from app.models.formula import Formula, FormulaHerb
    formula = db.query(Formula).filter(Formula.id == formula_id).first()
    if not formula:
        raise HTTPException(status_code=404, detail="方剂不存在")

    update_data = data.model_dump(exclude_unset=True)
    herbs_data = update_data.pop("herbs", None)

    for key, value in update_data.items():
        setattr(formula, key, value)

    if herbs_data:
        db.query(FormulaHerb).filter(FormulaHerb.formula_id == formula_id).delete()
        for herb in herbs_data:
            fh = FormulaHerb(
                formula_id=formula_id,
                herb_id=herb["herb_id"],
                herb_name=herb.get("herb_name"),
                dosage=herb.get("dosage"),
                role=herb.get("role", "assistant"),
                sort_order=herb.get("sort_order", 0),
            )
            db.add(fh)

    db.commit()
    db.refresh(formula)
    return formula


@router.delete("/{formula_id}")
async def delete_formula(
    formula_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """删除方剂（admin）"""
    success = FormulaService.delete_formula(db, formula_id) if hasattr(FormulaService, 'delete_formula') else None
    if success is None:
        from app.models.formula import Formula
        formula = db.query(Formula).filter(Formula.id == formula_id).first()
        if not formula:
            raise HTTPException(status_code=404, detail="方剂不存在")
        db.delete(formula)
        db.commit()
    return {"message": "删除成功"}


@router.get("/by-herb/{herb_id}", response_model=list[FormulaResponse])
async def get_formulas_by_herb(herb_id: int, db: Session = Depends(get_db)):
    """根据草药查询相关方剂"""
    return FormulaService.get_formulas_by_herb(db, herb_id)
