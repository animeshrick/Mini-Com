from typing import Optional

from django.db import transaction
from rest_framework import serializers

from auth_api.models import User
from cart.models import Cart
from order.export_types.request_data_type.create_order import CreateOrderRequest
from order.models.order import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    def validate(self, data: Optional[CreateOrderRequest] = None) -> bool:
        try:
            user = User.objects.get(id=data.user_id, is_deleted=False, is_active=True)
        except User.DoesNotExist:
            raise ValueError("User not found or is inactive")

        try:
            cart = Cart.objects.get(id=data.cart_id, is_active=True)
        except Cart.DoesNotExist:
            raise ValueError("Cart not found or is inactive")

        if cart:
            for cart_item in cart.cart_items.all():
                if cart_item.quantity > cart_item.product.stock:
                    raise ValueError("Out of stock")

        # check delivery_address is not None and str
        if not data.delivery_address or not isinstance(data.delivery_address, str):
            raise ValueError("Delivery address is required and must be a string")

        return True

    @transaction.atomic  # Ensures all DB operations succeed or rollback
    def create(self, data: CreateOrderRequest) -> Optional[Order]:
        if not self.validate(data):
            return None

        user = User.objects.get(id=data.user_id)
        cart = Cart.objects.get(id=data.cart_id)

        latest_order_no = Order.objects.filter(id=data.user_id).all().count()
        if latest_order_no:
            order_no = latest_order_no + 1
        else:
            order_no = 1
        user.order_no = order_no
        cart.is_active = False

        order = Order.objects.create(
            cart=cart,
            user=user,
            total_discount=0,
            coupon_code=None,
            delivery_address=data.delivery_address,
            delivery_date=None,
            pg_type=data.pg_type if data.pg_type else "COD",
            is_paid=True if data.pg_type != "COD" else False,
        )

        user.save()
        cart.save()

        return order
