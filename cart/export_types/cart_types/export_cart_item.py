from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from product_inventory.models import Product


class ExportCartItem(BaseModel):
    id: Optional[UUID]
    product: Optional[Product] = None
    quantity: Optional[str] = None

    def __init__(self, **kwargs):
        # if kwargs.get("category"):
        #     kwargs["category"] = ExportCategory(
        #         **kwargs["category"].model_to_dict()
        #     )
        super().__init__(**kwargs)


class ExportCartItemList(BaseModel):
    cart_items: List[ExportCartItem]
