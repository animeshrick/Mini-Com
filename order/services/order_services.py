import logging
from typing import Optional

from psycopg2 import DatabaseError

from cart.models import Cart
from helper.helper_log import onion
from order.export_types.order_types.export_order import ExportOrder, ExportOrderList
from order.export_types.request_data_type.create_order import CreateOrderRequest
from order.export_types.request_data_type.get_order import GetOrderRequest
from order.models.order import Order
from order.models.ordered_item import OrderedItem
from order.serializer.order_serializer import OrderSerializer


class OrderServices:
    @staticmethod
    def place_order(request_data: CreateOrderRequest)->Optional[ExportOrder]:
        try:
            order = OrderSerializer().create(request_data)
            if not order:
                logging.error("Order creation failed - serializer returned None")
                return None

            user_cart = Cart.objects.get(id=request_data.cart_id)

            total_price=0
            for cart_item in user_cart.cart_items.all():
                total_price = cart_item.product.price * cart_item.quantity

            cart_items =  len(user_cart.cart_items.all())

            export_cart = ExportOrder(
                id=order.id,
                user=order.user,
                cart=order.cart,
                pg_type=order.pg_type,
                total_items=cart_items,
                total_price=total_price,
                ordered_items=list(user_cart.cart_items.all()),
            )

            # user_cart.delete()

            return export_cart
        except ValueError as ve:
            # Validation errors from serializer
            logging.error(f"Validation error in order service: {str(ve)}")
            raise ve

        except Exception as e:
            # Unexpected errors
            logging.error(f"Unexpected error in order service: {str(e)}", exc_info=True)
            return None

    @staticmethod
    def get_order_list(request_data: GetOrderRequest)-> Optional[ExportOrderList]:
        try:
            all_orders = Order.objects.filter(user__id=request_data.user_id)
        except Exception:
            raise DatabaseError()

        if all_orders:
            all_orders = all_orders.prefetch_related("order")

            order_list = []
            for order in all_orders:
                ordered_items = list(order.order.all())

                total_items = sum(item.quantity for item in ordered_items)
                total_price = sum(item.quantity * item.product.price for item in ordered_items)

                order_list.append(
                    ExportOrder(
                        **order.model_to_dict(),
                        ordered_items=ordered_items,
                        total_items=total_items,
                        total_price=total_price,
                    )
                )

            user_orders = ExportOrderList(order_list=order_list)
            return user_orders
        return None