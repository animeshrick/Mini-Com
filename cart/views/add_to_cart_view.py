from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exception_handlers import ExceptionHandler
from cart.export_types.request_data_types.add_update_delete import AddUpdatedDeleteCartRequestType
from cart.services.cart_services import CartServices


class AddUpdateDeleteCartView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request: Request):
        try:
            result = CartServices.add_update_delete_cart_service(
                request_data=AddUpdatedDeleteCartRequestType(**request.data)
            )
            if result:
                return Response(
                    data={
                        "message": "You are good to go",
                        "data": "result.model_dump()",
                    },
                    status=status.HTTP_201_CREATED,
                    content_type="application/json",
                )
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
