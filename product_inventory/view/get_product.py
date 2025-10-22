from uuid import UUID

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exception_handlers import ExceptionHandler
from product_inventory.export_types.product_types.export_product import ExportProduct
from product_inventory.models import Product
from product_inventory.services.product_service import ProductService


class GetProductView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            if not request.data.get("product_id"):
                raise ValueError("product_id is required.")
            try:
                product_uuid = UUID(request.data.get("product_id"))
            except Exception:
                raise ValueError("Invalid product_id format. Must be a valid UUID.")
            product = ProductService().get_product_service(product_id=str(product_uuid))

            similar_items = [
                ExportProduct(**p.model_to_dict()).model_dump()
                for p in Product.objects.filter(category_id=product.category.id).exclude(id=product.id)[:5]
            ]

            return Response(
                data={
                    "message": "Product details fetched Successfully.",
                    "data": {
                        "parent_product": product.model_dump(),
                        "similar_items": similar_items,
                    },
                },
                status=status.HTTP_200_OK,
                content_type="application/json",
            )
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
