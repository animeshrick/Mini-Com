from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


class ProductItem(BaseModel):
    product_id: UUID
    quantity: int = Field(default=1, ge=0)


class AddUpdatedDeleteCartRequestType(BaseModel):
    user_id: Optional[UUID] = None
    products: Optional[List[ProductItem]] = None
    action: str  # A/U/D
