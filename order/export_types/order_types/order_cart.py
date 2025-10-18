from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class ExportOrderCart(BaseModel):
    id: UUID
    total_item: Optional[str] = None
    total_price: Optional[str] = None

