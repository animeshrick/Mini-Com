from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from cart.export_types.cart_types.cart_user import ExportCartUser
from cart.export_types.cart_types.export_cart_item import ExportCartItemList, ExportCartItem


class ExportCart(BaseModel):
    id: Optional[UUID]
    user: Optional[ExportCartUser]
    cart_items: Optional[ExportCartItemList] = None
    is_active: Optional[bool] = None

    def __init__(self, **kwargs):
        if kwargs.get("user"):
            kwargs["user"] = ExportCartUser(
                **kwargs["user"].model_to_dict()
            )
        if kwargs.get("cart_items"):
            cart_items_list = kwargs["cart_items"]
            # Create ExportCartItemList with cart_items as a list
            kwargs["cart_items"] = ExportCartItemList(
                cart_items=[
                    ExportCartItem(**item.model_to_dict())
                    for item in cart_items_list
                ]
            )
        super().__init__(**kwargs)


class ExportCartList(BaseModel):
    cart_list: List[ExportCart]
