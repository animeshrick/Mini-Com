from typing import Optional, List
from uuid import UUID
from _decimal import Decimal

from pydantic import BaseModel

from order.export_types.order_types.export_ordered_item import ExportOrderedItem


class ExportOrder(BaseModel):
    id: Optional[UUID]
    pg_type: Optional[str] = None
    total_items: Optional[int] = None
    total_price: Optional[Decimal] = None
    ordered_items: Optional[List[ExportOrderedItem]] = None

    def __init__(self, **kwargs):
        if kwargs.get("ordered_items"):
            cart_items_list = kwargs["ordered_items"]
            if isinstance(cart_items_list, list):
                kwargs["ordered_items"] = [
                    ExportOrderedItem(**item.model_to_dict())
                    for item in cart_items_list
                ]
            elif hasattr(cart_items_list, 'all'):
                kwargs["ordered_items"] = [
                    ExportOrderedItem(**item.model_to_dict())
                    for item in cart_items_list.all()
                ]
        super().__init__(**kwargs)


class ExportOrderList(BaseModel):
    cart_list: List[ExportOrder]
