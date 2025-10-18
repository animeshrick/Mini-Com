from typing import Optional, List
from uuid import UUID
from _decimal import Decimal

from pydantic import BaseModel

from cart.export_types.cart_types.cart_user import ExportCartUser
from order.export_types.order_types.order_cart import ExportOrderCart


class ExportOrder(BaseModel):
    id: Optional[UUID]
    user: Optional[ExportCartUser]
    cart: Optional[ExportOrderCart] = None
    pg_type: Optional[str] = None
    total_items: Optional[int] = None
    total_price: Optional[Decimal] = None

    def __init__(self, **kwargs):
        if kwargs.get("user"):
            kwargs["user"] = ExportCartUser(
                **kwargs["user"].model_to_dict()
            )
        if kwargs.get("cart"):
            kwargs["cart"] = ExportOrderCart(
                **kwargs["cart"].model_to_dict()
            )
        super().__init__(**kwargs)


class ExportOrderList(BaseModel):
    cart_list: List[ExportOrder]
