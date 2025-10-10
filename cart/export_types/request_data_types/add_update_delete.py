from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class AddUpdatedDeleteCartRequestType(BaseModel):
    user_id: Optional[UUID] = None
    products: Optional[List] = None
    action: str  # A/U/D
