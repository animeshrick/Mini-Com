from typing import Optional
from pydantic import BaseModel


class FilterProductRequestType(BaseModel):
    query: Optional[str] = None