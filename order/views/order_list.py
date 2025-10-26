from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exception_handlers import ExceptionHandler
from order.export_types.request_data_type.get_order import GetOrderRequest
from order.services.order_services import OrderServices


class OrderListView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request: Request):
        try:
            result = OrderServices.get_order_list(
                request_data=GetOrderRequest(**request.data)
            )
            if result:
                return Response(
                    data={
                        "message": "Your order(s).",
                        "data": result.model_dump(),
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                return Response(
                    data={
                        "message": "We are sorry, something is not right with your order(s).",
                        "data": [],
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content_type="application/json",
                )
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
