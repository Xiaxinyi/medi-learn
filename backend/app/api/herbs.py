from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database import get_db
from app.schemas.herb import HerbCreate, HerbUpdate, HerbResponse, HerbListResponse, HerbAttributeCreate, HerbAttributeResponse
from app.schemas.common import PageResult
from app.services.herb_service import HerbService
from app.services.ai_service import AIService
from app.middleware.auth_middleware import get_current_user, get_current_admin

router = APIRouter()


@router.get("/attributes", response_model=List[HerbAttributeResponse])
async def list_attributes(db: Session = Depends(get_db)):
    """获取所有属性标签"""
    return HerbService.list_attributes(db)


@router.post("/attributes", response_model=HerbAttributeResponse)
async def create_attribute(
    data: HerbAttributeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """创建属性标签（admin）"""
    from app.models.herb import HerbAttribute
    attr = HerbAttribute(**data.model_dump())
    db.add(attr)
    db.commit()
    db.refresh(attr)
    return attr


@router.get("/", response_model=PageResult[HerbResponse])
async def list_herbs(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    attribute: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取草药列表"""
    herbs, total = HerbService.list_herbs(db, search, category, attribute, page, page_size)
    return {
        "items": herbs,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("/generate")
async def generate_herb_info(
    name: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """AI生成草药信息（admin）"""
    categories = [
        '解表药', '清热药', '泻下药', '祛风湿药', '化湿药', '利水渗湿药',
        '温里药', '理气药', '消食药', '驱虫药', '止血药', '活血化瘀药',
        '化痰止咳平喘药', '安神药', '平肝息风药', '开窍药', '补益药', '收涩药'
    ]
    try:
        result = await AIService.generate_herb_info(name, categories)
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI生成失败: {str(e)}")


@router.get("/{herb_id}", response_model=HerbResponse)
async def get_herb(herb_id: int, db: Session = Depends(get_db)):
    """获取草药详情"""
    herb = HerbService.get_herb(db, herb_id)
    if not herb:
        raise HTTPException(status_code=404, detail="草药不存在")
    return herb


@router.post("/", response_model=HerbResponse)
async def create_herb(
    data: HerbCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """添加草药（admin）"""
    herb = HerbService.create_herb(db, **data.model_dump())
    return herb


@router.put("/{herb_id}", response_model=HerbResponse)
async def update_herb(
    herb_id: int,
    data: HerbUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """更新草药（admin）"""
    herb = HerbService.update_herb(db, herb_id, **data.model_dump(exclude_unset=True))
    if not herb:
        raise HTTPException(status_code=404, detail="草药不存在")
    return herb


@router.delete("/{herb_id}")
async def delete_herb(
    herb_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """删除草药（admin）"""
    success = HerbService.delete_herb(db, herb_id)
    if not success:
        raise HTTPException(status_code=404, detail="草药不存在")
    return {"message": "删除成功"}
