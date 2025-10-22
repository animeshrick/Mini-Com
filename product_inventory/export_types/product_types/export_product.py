from _decimal import Decimal
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from product_inventory.export_types.product_types.export_category import ExportCategory


class ExportProduct(BaseModel):
    id: Optional[UUID]
    name: Optional[str] = None
    slug: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None
    image: Optional[str] = None
    category: Optional[ExportCategory] = None
    brand: Optional[str] = None
    discount: Optional[Decimal] = None
    # similar_type_items: Optional[List[ExportProduct]] = None
    is_active: bool

    def __init__(self, **kwargs):
        if kwargs.get("category"):
            kwargs["category"] = ExportCategory(
                **kwargs["category"].model_to_dict()
            )
        super().__init__(**kwargs)


class ExportProductList(BaseModel):
    product_list: List[ExportProduct]
