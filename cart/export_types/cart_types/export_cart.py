from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from auth_api.models import User
from cart.export_types.cart_types.export_cart_item import ExportCartItemList


class ExportCart(BaseModel):
    id: Optional[UUID]
    user: Optional[User]
    cart_items: Optional[ExportCartItemList]
    is_active: Optional[bool] = None

    def __init__(self, **kwargs):
        # if kwargs.get("category"):
        #     kwargs["category"] = ExportCategory(
        #         **kwargs["category"].model_to_dict()
        #     )
        super().__init__(**kwargs)


class ExportCartList(BaseModel):
    cart_list: List[ExportCart]
