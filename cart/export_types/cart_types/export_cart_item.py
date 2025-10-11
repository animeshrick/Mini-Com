from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict

# Import the Pydantic model for a Product, not the Django model
from product_inventory.export_types.product_types.export_product import ExportProduct
# We still need the Django model for the type check in __init__
from product_inventory.models import Product


class ExportCartItem(BaseModel):
    # This config is still good practice, so we'll keep it.
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[UUID]
    # The field should be typed with the Pydantic model
    product: Optional[ExportProduct] = None
    quantity: Optional[int] = None  # Quantity should be a number

    def __init__(self, **kwargs):
        # When we create this Pydantic model from a Django model,
        # the 'product' kwarg will be a Django Product object.
        # We need to manually convert it to an ExportProduct Pydantic model.
        product_instance = kwargs.get("product")
        if product_instance and isinstance(product_instance, Product):
            kwargs["product"] = ExportProduct(**product_instance.model_to_dict())
        super().__init__(**kwargs)


class ExportCartItemList(BaseModel):
    cart_items: List[ExportCartItem]
