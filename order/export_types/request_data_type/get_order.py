from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class GetOrderRequest(BaseModel):
    user_id: UUID
    from_date: Optional[str] = None
    to_date: Optional[str] = None