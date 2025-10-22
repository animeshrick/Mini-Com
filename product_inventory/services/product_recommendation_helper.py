import pandas as pd
import logging

from order.models.order import Order
from product_inventory.services.product_recommender import ProductRecommender


class ProductRecommendationHelper:
    """
    Handles fetching order data and preparing input for the recommendation model.
    """

    _logger = logging.getLogger(__name__)

    @staticmethod
    def _load_user_order_data():
        records = []
        try:
            orders = Order.objects.prefetch_related('order').select_related('user').all()

            for order in orders:
                for item in order.order.all():
                    if item.product and item.product.name:  # skip nulls
                        records.append({
                            'user_id': str(order.user.id),  # convert UUID → string
                            'ordered_items': item.product.name,
                            'quantity': item.quantity,
                            'order_created_datetime': order.created_at
                        })

            df = pd.DataFrame(records)
            # print(f"df['user_id']: {df['user_id']}")
            # ProductRecommendationHelper._logger.debug(f"data_df: {df}")
            # if not orders.empty: # Check if orders is not empty before accessing orders[0]
            #     ProductRecommendationHelper._logger.debug(f"Onion: {df[df['user_id'] == str(orders[0].user.id)]}")
            #     ProductRecommendationHelper._logger.debug(f"Onion2: {str(orders[0].user.id)}")
            # ProductRecommendationHelper._logger.debug(f"Onion1: {df['user_id']}")

            return df
        except Exception as e:
            ProductRecommendationHelper._logger.error(f"Error loading user order data: {e}")
            return pd.DataFrame() # Return an empty DataFrame in case of an error

    @classmethod
    def get_recommendations(cls, user_id):
        df = cls._load_user_order_data()

        recommender = ProductRecommender(df)
        recommendations = recommender.recommend_for_user(user_id)
        # recommender.visualize_matrix()

        # return top N with pretty formatting
        result = [
            {"product": item, "predicted_score": round(score, 2)}
            for item, score in recommendations
            if score > -1e10
        ]

        # Initialize an empty list to hold the results
        # result = []
        #
        # # Loop through each tuple in the recommendations list
        # for item, score in recommendations:
        #     print(f"recommendations: {recommendations}")
        #     # Create a new dictionary with the desired format
        #     formatted_recommendation = {
        #         "product": item,
        #         "predicted_score": round(score, 2)
        #     }
        #     print(f"formatted_recommendation: {formatted_recommendation}")
        #     result.append(formatted_recommendation)
        #     print(f"result: {result}")

        print(f"get_recommendations_result: {result}")
        return result
