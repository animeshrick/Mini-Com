from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class FetchCartRequestType(BaseModel):
    user_id: UUID