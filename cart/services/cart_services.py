from typing import Optional

from cart.export_types.cart_types.export_cart import ExportCart
from cart.export_types.request_data_types.add_update_delete import AddUpdatedDeleteCartRequestType
from cart.export_types.request_data_types.delete_cart import DeleteCartRequestType
from cart.export_types.request_data_types.fetch_cart import FetchCartRequestType
from cart.models import Cart
from cart.serializers.cart_serializer import CartSerializer
import logging
from decimal import Decimal
from helper_log import onion


class CartServices:

    @staticmethod
    def add_update_delete_cart_service(
            request_data: AddUpdatedDeleteCartRequestType
    ) -> Optional[ExportCart]:
        """
        Handle cart operations (Add/Update/Delete)

        Args:
            request_data: Contains user_id, action (A/U/D), and products list

        Returns:
            ExportCart: Serialized cart data for API response
            None: If operation fails
        """
        try:
            # Create/update cart using serializer
            cart: Cart = CartSerializer().create(request_data)

            if not cart:
                logging.error("Cart creation/update failed - serializer returned None")
                return None

            # Convert Django Cart model to Pydantic ExportCart
            user_cart = ExportCart(
                id=cart.id,
                user=cart.user,
                cart_items=list(cart.cart_items.all()),  # Use cart_items (related_name)
                is_active=cart.is_active,
                total_cart_price=getattr(cart, 'total_cart_price', 0.0)
            )

            onion("add_update_delete_cart_service",
                f"Cart operation successful: Cart ID {cart.id}, "
                f"User {cart.user.email}, Total: ₹{user_cart.total_cart_price}"
            )
            return user_cart

        except ValueError as ve:
            # Validation errors from serializer
            onion("add_update_delete_cart_service_ValueError", f"Validation error in cart service: {str(ve)}")
            raise ve

        except Exception as e:
            # Unexpected errors
            onion("add_update_delete_cart_service_Exception", f"Unexpected error in cart service: {str(e)}")
            return None

    @staticmethod
    def fetch_cart(request_data: FetchCartRequestType)-> Optional[ExportCart]:
        try:
            cart = Cart.objects.get(user__id=request_data.user_id, is_active=True)
            if cart:
                export_cart = ExportCart(
                    id=cart.id,
                    user=cart.user,
                    cart_items=list(cart.cart_items.all()),  # Use cart_items (related_name)
                    is_active=cart.is_active,
                    total_cart_price=CartServices().total_cart_value(cart)
                )

                onion("fetch_cart",
                    f"Cart sync operation successful: Cart ID {cart.id}, "
                    f"User {cart.user.email}, Total: ₹{export_cart.total_cart_price}"
                )
                return export_cart
        except Cart.DoesNotExist:
            onion("fetch_cart_DoesNotExist",f"Cart not found for user_id: {request_data.user_id}")
            return ExportCart()
        return None

    @staticmethod
    def total_cart_value(cart: Cart) -> Decimal:
        if not cart:
            return Decimal('0.00')

        total = Decimal('0.00')

        # Access cart items using the related_name
        for cart_item in cart.cart_items.all():
            if cart_item.product and cart_item.quantity:
                # Calculate: product.price * quantity
                item_subtotal = cart_item.product.price * cart_item.quantity
                total += item_subtotal

        return total

    @staticmethod
    def delete_cart(request_data: DeleteCartRequestType)-> bool:
        try:
            cart = Cart.objects.get(user__id=request_data.user_id, is_active=True)
            if cart.is_active:
                cart.is_active = False
                cart.save()
                return True
        except Cart.DoesNotExist:
            onion("delete_cart_DoesNotExist",f"Cart not found for user_id: {request_data.user_id}")
            return False

        return False