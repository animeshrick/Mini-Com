from typing import Optional

from psycopg2 import DatabaseError

from helper.helper_log import onion
from helper.spell_correcter import SpellCorrector
from product_inventory.export_types.product_types.export_product import ExportProductList, ExportProduct
from product_inventory.export_types.request_types.filter_product_request_type import FilterProductRequestType
from product_inventory.models.product import Product


class ProductService:
    @staticmethod
    def get_all_product_service(request_data: Optional[FilterProductRequestType]) -> Optional[ExportProductList]:
        try:
            get_all_products = Product.objects.all()
        except Exception:
            raise DatabaseError()

        user_query = request_data.query
        corrected_query = ""

        if user_query:
            #  and len(request_data.query)>=4

            if user_query:
                corrected_query = SpellCorrector().correct_spell(user_query=user_query)
                onion("user_query_corrected",f"User Input: {user_query} → Corrected: {corrected_query}")

            all_product = ExportProductList(
                product_list=[
                    ExportProduct(**product.model_to_dict())
                    for product in get_all_products
                    if product and (
                            (q := corrected_query.lower()) in (product.name or "").lower()
                            or q in (product.category.name if product.category else "").lower()
                            or q in (product.brand or "").lower()
                            or q in (product.description or "").lower())
                ]
            )
            return all_product

        elif get_all_products and not user_query:
            all_product = ExportProductList(
                product_list=[
                    ExportProduct(**product.model_to_dict())
                    for product in get_all_products
                ]
            )
            return all_product
        else:
            return None

    @staticmethod
    def get_product_service(product_id: str) -> Optional[ExportProduct]:
        try:
            product = Product.objects.get(id=product_id)
        except Exception:
            raise ValueError("This product is not listed.")
        if product:
            return ExportProduct(**product.model_to_dict())
        else:
            return None
