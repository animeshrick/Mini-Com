from typing import Optional

from cart.export_types.cart_types.export_cart import ExportCart
from cart.export_types.request_data_types.add_update_delete import AddUpdatedDeleteCartRequestType
from cart.models import Cart
from cart.serializers.cart_serializer import CartSerializer
import logging


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

            logging.info(
                f"Cart operation successful: Cart ID {cart.id}, "
                f"User {cart.user.email}, Total: ₹{user_cart.total_cart_price}"
            )
            return user_cart

        except ValueError as ve:
            # Validation errors from serializer
            logging.error(f"Validation error in cart service: {str(ve)}")
            raise ve

        except Exception as e:
            # Unexpected errors
            logging.error(f"Unexpected error in cart service: {str(e)}", exc_info=True)
            return None