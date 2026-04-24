from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class HerbAttributeBase(BaseModel):
    name: str
    group_name: Optional[str] = None
    color: Optional[str] = None


class HerbAttributeCreate(HerbAttributeBase):
    pass


class HerbAttributeResponse(HerbAttributeBase):
    id: int
    is_system: int = 1
    created_at: datetime

    class Config:
        from_attributes = True


class HerbImageResponse(BaseModel):
    id: int
    image_url: str
    thumbnail_url: Optional[str] = None
    sort_order: int = 0
    is_cover: int = 0

    class Config:
        from_attributes = True


class HerbNoteResponse(BaseModel):
    id: int
    user_id: int
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class HerbBase(BaseModel):
    name: str
    latin_name: Optional[str] = None
    aliases: Optional[List[str]] = None
    efficacy: Optional[str] = None
    indications: Optional[str] = None
    dosage: Optional[str] = None
    contraindications: Optional[str] = None
    category: Optional[str] = None
    origin: Optional[str] = None


class HerbCreate(HerbBase):
    attribute_ids: Optional[List[int]] = None
    image_urls: Optional[List[str]] = None


class HerbUpdate(BaseModel):
    name: Optional[str] = None
    latin_name: Optional[str] = None
    aliases: Optional[List[str]] = None
    efficacy: Optional[str] = None
    indications: Optional[str] = None
    dosage: Optional[str] = None
    contraindications: Optional[str] = None
    category: Optional[str] = None
    origin: Optional[str] = None
    attribute_ids: Optional[List[int]] = None


class HerbResponse(HerbBase):
    id: int
    is_system: int = 0
    created_at: datetime
    updated_at: datetime
    images: List[HerbImageResponse] = []
    attributes: List[HerbAttributeResponse] = []

    class Config:
        from_attributes = True


class HerbListResponse(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    efficacy: Optional[str] = None
    cover_image: Optional[str] = None
    is_system: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class HerbNoteCreate(BaseModel):
    content: str
