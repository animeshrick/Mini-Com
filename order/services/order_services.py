import logging
from typing import Optional

from order.export_types.order_types.export_order import ExportOrder
from order.export_types.request_data_type.create_order import CreateOrderRequest
from order.serializer.order_serializer import OrderSerializer


class OrderServices:
    @staticmethod
    def place_order(request_data: CreateOrderRequest)->Optional[ExportOrder]:
        try:
            order = OrderSerializer.create(request_data)
            if not order:
                logging.error("Order creation failed - serializer returned None")
                return None

            total_price =  order.cart.total_cart_price
            cart_items =  len(order.cart.cart_items)

            return ExportOrder(
                id=order.id,
                user=order.user,
                cart=order.cart,
                pg_type=order.pg_type,
                total_items=cart_items,
                total_price=total_price,
            )
        except ValueError as ve:
            # Validation errors from serializer
            logging.error(f"Validation error in order service: {str(ve)}")
            raise ve

        except Exception as e:
            # Unexpected errors
            logging.error(f"Unexpected error in order service: {str(e)}", exc_info=True)
            return None