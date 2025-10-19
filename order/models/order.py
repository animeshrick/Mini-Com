from django.db import models

from auth_api.models import User
from auth_api.models.base_models.base_model import GenericBaseModel
from cart.models.cart import Cart
from order.models.enum.order_status import OrderStatus


class Order(GenericBaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)

    delivery_address = models.CharField(max_length=500)
    delivery_date = models.CharField(max_length=500, blank=True, null=True)

    pg_type = models.CharField(max_length=100)

    is_paid = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    order_status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PLACED,
    )

    class Meta:
        indexes = [
            models.Index(fields=["cart"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.user.name}'s order {self.id}"
