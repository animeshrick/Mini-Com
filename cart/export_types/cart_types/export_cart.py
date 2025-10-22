from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel
from _decimal import Decimal

from cart.export_types.cart_types.cart_user import ExportCartUser
from cart.export_types.cart_types.export_cart_item import ExportCartItem


class ExportCart(BaseModel):
    id: Optional[UUID] = None
    user: Optional[ExportCartUser] = None
    cart_items: Optional[List[ExportCartItem]] = None
    total_cart_price: Optional[Decimal] = None
    is_active: Optional[bool] = None

    def __init__(self, **kwargs):
        if kwargs.get("user"):
            kwargs["user"] = ExportCartUser(
                **kwargs["user"].model_to_dict()
            )
        if kwargs.get("cart_items"):
            cart_items_list = kwargs["cart_items"]
            if isinstance(cart_items_list, list):
                kwargs["cart_items"] = [
                    ExportCartItem(**item.model_to_dict())
                    for item in cart_items_list
                ]
            elif hasattr(cart_items_list, 'all'):
                kwargs["cart_items"] = [
                    ExportCartItem(**item.model_to_dict())
                    for item in cart_items_list.all()
                ]
        super().__init__(**kwargs)


class ExportCartList(BaseModel):
    cart_list: List[ExportCart]
