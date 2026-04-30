from typing import List, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PageResult(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
