from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class ExportCartUser(BaseModel):
    id: UUID
    email: Optional[str] = None
    full_name: Optional[str] = None