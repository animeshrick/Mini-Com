import pandas as pd
import logging

from order.models.order import Order
from product_inventory.services.product_recommender import ProductRecommender


class ProductRecommendationHelperV2:
    # optimize it to max also make dict where {p_name: qty, ordered_data: value}
    @staticmethod
    def get_ordered_items(user_id: str) -> dict:
        """
        Retrieves a dictionary of ordered items for a given user, optimized for performance.
        The dictionary format is {product_name: {'quantity': qty, 'ordered_date': date}}.
        """
        # Use select_related and prefetch_related for optimized database queries
        orders = Order.objects.filter(user_id=user_id).select_related('user').prefetch_related('order')

        ordered_items = {}
        for order in orders:
            for item in order.order.all():
                ordered_items = {'id': item.product.id,'name': item.product.name , 'quantity': item.quantity, 'ordered_date': order.created_at}
        print(f"ordered_items: {ordered_items}")
        return ordered_items
