from django.urls import path

from product_inventory.view.get_all_products import AllProductView
from product_inventory.view.get_product import GetProductView
from product_inventory.view.product_recommendation_view import GetProductReCommendationView

urlpatterns = [
    path("all_product", AllProductView.as_view(), name="All-product"),
    path("get_product", GetProductView.as_view(), name="Get-product"),
    path("recommendations", GetProductReCommendationView.as_view(), name="Recommendations"),
]
