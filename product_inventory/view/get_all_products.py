from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exception_handlers import ExceptionHandler
from helper.helper_log import onion
from product_inventory.export_types.product_types.export_product import ExportProductList
from product_inventory.export_types.request_types.filter_product_request_type import FilterProductRequestType
from product_inventory.services.product_service import ProductService


class AllProductView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
            query = request.query_params.get("query", None)
            all_product = ProductService().get_all_product_service(
                request_data=FilterProductRequestType(query=query)
            )

            product_list = (
                all_product.model_dump().get("product_list", [])
                if all_product and isinstance(all_product, ExportProductList)
                else []
            )

            onion("filter_products", str(len(product_list)))

            message = (
                "Data fetched successfully."
                if product_list
                else f"Sorry, we can’t fulfill your request ['{query}']."
            )

            return Response(
                data={"message": message, "data": product_list},
                status=status.HTTP_200_OK,
                content_type="application/json",
            )

        except Exception as e:
            return ExceptionHandler().handle_exception(e)
