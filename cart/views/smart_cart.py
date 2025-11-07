from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cart.services.cart_helper import CartHelper


class SmartCartView(APIView):
    """
    API endpoint to get personalized product recommendations for a user.
    """

    def get(self, request):
        text = request.query_params.get('text')
        CartHelper.extract_products(text)

        try:
            return Response(
                data={
                    "message": "Smart Cart executed successfully",
                    "data": [],
                },
                status=status.HTTP_200_OK,
                content_type="application/json",
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
