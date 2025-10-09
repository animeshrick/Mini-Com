from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exception_handlers import ExceptionHandler
from product_inventory.export_types.product_types.export_product import ExportProductList
from product_inventory.services.product_service import ProductService


class AllProductView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, _):
        try:
            all_product = ProductService().get_all_product_service()
            if all_product and isinstance(all_product, ExportProductList):
                return Response(
                    data={
                        "message": "Data fetched successfully.",
                        "data": all_product.model_dump(),
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                return Response(
                    data={
                        "data": {"user_list": []},
                        "message": "Currently we arr shortage of products",
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
