from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exception_handlers import ExceptionHandler
from cart.export_types.request_data_types.add_update_delete import AddUpdatedDeleteCartRequestType
from cart.export_types.request_data_types.fetch_cart import FetchCartRequestType
from cart.services.cart_services import CartServices


class FetchCartView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request: Request):
        try:
            result = CartServices.fetch_cart(
                request_data=FetchCartRequestType(**request.data)
            )
            cart_id = result.id
            if cart_id:
                return Response(
                    data={
                        "message": "Your cart is synced.",
                        "data": result.model_dump(),
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                return Response(
                    data={
                        "message": "We are sorry, something is not right in your cart!",
                        "data": [],
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content_type="application/json",
                )
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
