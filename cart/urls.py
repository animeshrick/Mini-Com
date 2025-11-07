from django.urls import path

from cart.views.add_to_cart_view import AddUpdateDeleteCartView
from cart.views.delete_cart import DeleteCartView
from cart.views.fetch_cart import FetchCartView
from cart.views.smart_cart import SmartCartView

urlpatterns = [
    path("add_update_delete_cart", AddUpdateDeleteCartView.as_view(), name="Add-update-delete-to-cart"),
    path("delete_cart", DeleteCartView.as_view(), name="Remove-cart"),
    path("cart_sync", FetchCartView.as_view(), name="Fetch-cart"),
    path("smart_cart", SmartCartView.as_view(), name="Smart-cart"),
]
