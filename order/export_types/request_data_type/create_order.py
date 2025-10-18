from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CreateOrderRequest(BaseModel):
    cart_id: UUID
    user_id: UUID
    delivery_address: str
    pg_type: Optional[str] = None