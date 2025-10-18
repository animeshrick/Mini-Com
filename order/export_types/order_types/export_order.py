from typing import Optional, List
from uuid import UUID
from _decimal import Decimal

from pydantic import BaseModel


class ExportOrder(BaseModel):
    id: Optional[UUID]
    pg_type: Optional[str] = None
    total_items: Optional[int] = None
    total_price: Optional[Decimal] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ExportOrderList(BaseModel):
    cart_list: List[ExportOrder]
