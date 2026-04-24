from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class FormulaHerbBase(BaseModel):
    herb_id: int
    herb_name: Optional[str] = None
    dosage: Optional[str] = None
    role: str = "assistant"  # chief, deputy, assistant, envoy
    sort_order: int = 0


class FormulaHerbCreate(FormulaHerbBase):
    pass


class FormulaHerbResponse(FormulaHerbBase):
    id: int
    formula_id: int

    class Config:
        from_attributes = True


class FormulaBase(BaseModel):
    name: str
    source: Optional[str] = None
    category: Optional[str] = None
    indications: Optional[str] = None
    usage: Optional[str] = None
    modifications: Optional[str] = None
    precautions: Optional[str] = None


class FormulaCreate(FormulaBase):
    herbs: List[FormulaHerbCreate]


class FormulaUpdate(BaseModel):
    name: Optional[str] = None
    source: Optional[str] = None
    category: Optional[str] = None
    indications: Optional[str] = None
    usage: Optional[str] = None
    modifications: Optional[str] = None
    precautions: Optional[str] = None
    herbs: Optional[List[FormulaHerbCreate]] = None


class FormulaResponse(FormulaBase):
    id: int
    is_system: int = 0
    created_at: datetime
    updated_at: datetime
    herbs: List[FormulaHerbResponse] = []

    class Config:
        from_attributes = True


class FormulaListResponse(BaseModel):
    id: int
    name: str
    source: Optional[str] = None
    category: Optional[str] = None
    indications: Optional[str] = None
    is_system: int = 0
    created_at: datetime

    class Config:
        from_attributes = True
