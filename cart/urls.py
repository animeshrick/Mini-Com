from django.urls import path

from cart.views.add_to_cart_view import AddUpdateDeleteCartView

urlpatterns = [
    path("add_update_delete_cart", AddUpdateDeleteCartView.as_view(), name="Add-update-delete-to-cart"),
    # path("delete_cart", AddToCartView.as_view(), name="Remove-cart"),
    # path("view_cart", AddToCartView.as_view(), name="View-cart"),
]
