from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class DeleteCartRequestType(BaseModel):
    user_id: Optional[UUID] = None