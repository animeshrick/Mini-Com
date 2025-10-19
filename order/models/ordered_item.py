from django.db import models

from auth_api.models.base_models.base_model import GenericBaseModel
from cart.models.cart import Cart
from order.models.order import Order
from product_inventory.models import Product


class OrderedItem(GenericBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'product')  # Prevent same product multiple times in one cart
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["product"]),
        ]

    def __str__(self):
        return f"{self.product.stock} x {self.product.name} in cart {self.order.id}"

    def subtotal(self):
        return self.product.price * self.quantity
