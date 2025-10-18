from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exception_handlers import ExceptionHandler
from order.export_types.request_data_type.create_order import CreateOrderRequest
from order.services.order_services import OrderServices


class PlaceOrderView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request: Request):
        try:
            result = OrderServices.place_order(
                request_data=CreateOrderRequest(**request.data)
            )
            if result:
                return Response(
                    data={
                        "message": "You order is placed",
                        "data": result.model_dump(),
                    },
                    status=status.HTTP_201_CREATED,
                    content_type="application/json",
                )
            else:
                return Response(
                    data={
                        "message": "We are sorry, something is not right!",
                        "data": [],
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content_type="application/json",
                )
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
