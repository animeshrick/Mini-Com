from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product_inventory.services.product_recommendation_helper import ProductRecommendationHelper


class GetProductReCommendationView(APIView):
    """
    API endpoint to get personalized product recommendations for a user.
    """

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response(
                {"error": "user_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            recommendations = ProductRecommendationHelper.get_recommendations(user_id)
            return Response(
                data={
                    "message": "Product recommendations fetched Successfully.",
                    "data": recommendations,
                },
                status=status.HTTP_200_OK,
                content_type="application/json",
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
