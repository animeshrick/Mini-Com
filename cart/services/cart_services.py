from typing import Optional

from cart.export_types.cart_types.export_cart import ExportCart
from cart.export_types.request_data_types.add_update_delete import AddUpdatedDeleteCartRequestType
from cart.models import Cart
from cart.serializers.cart_serializer import CartSerializer


class CartServices:

    @staticmethod
    def add_update_delete_cart_service(request_data: AddUpdatedDeleteCartRequestType) -> Optional[ExportCart]:
        cart: Cart = CartSerializer().create(request_data)
        if cart:
            print(f"cart: {cart.id} {cart}")
            user_cart = ExportCart(with_id=True, **cart.model_to_dict())
            return user_cart
        else:
            return None