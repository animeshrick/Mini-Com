from typing import Optional

from rest_framework import serializers
from sqlalchemy.testing.suite.test_reflection import users

from auth_api.models import User
from cart.export_types.request_data_types.add_update_delete import AddUpdatedDeleteCartRequestType
from cart.models import Cart, CartItem
from product_inventory.models import Product


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"

    def validate(self, data: Optional[AddUpdatedDeleteCartRequestType] = None) -> Optional[bool]:
        user: User = User.objects.get(id=data.user_id, is_deleted=False, is_active=True)
        if not user:
            raise ValueError("User not found")

        is_add_action = data.action.upper() == "A"
        is_update_action = data.action.upper() == "U"
        is_delete_action = data.action.upper() == "D"

        if not is_add_action and not is_update_action and not is_delete_action:
            raise ValueError("Action must be A/U/D")

        if len(data.products) > 0:
            for item in data.products:
                user_product = Product.objects.get(id=item.product_id)
                if user_product.stock == 0:
                    raise ValueError("Product is not available.")
                if not user_product:
                    raise ValueError("Product not found or is not available.")
                if item.quantity <= 0:
                    raise ValueError("Quantity must be greater than zero.")


        return True

    def create(self, data: AddUpdatedDeleteCartRequestType) -> Optional[Cart]:
        if self.validate(data):
            user: User = User.objects.get(id=data.user_id)
            cart = Cart(
                user=user,
                is_active=True
            )
            cart.save()  # Must save first

            cart_items = []
            for cart_item in data.products:
                product = Product.objects.get(id=cart_item.product_id)
                item = CartItem(
                    cart=cart,
                    product=product,
                    quantity=cart_item.quantity
                )
                cart_items.append(item)
                product.stock -= cart_item.quantity
                product.save()

            CartItem.objects.bulk_create(cart_items)
            cart.refresh_from_db()  # Refresh to load relationships

            return cart
        return None