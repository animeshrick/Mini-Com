from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from product_inventory.export_types.product_types.export_product import ExportProduct
from product_inventory.models import Product


class ExportOrderedItem(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[UUID]
    product: Optional[ExportProduct] = None
    quantity: Optional[int] = None

    def __init__(self, **kwargs):
        product_instance = kwargs.get("product")
        if product_instance and isinstance(product_instance, Product):
            kwargs["product"] = ExportProduct(**product_instance.model_to_dict())
        super().__init__(**kwargs)
