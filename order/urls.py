from django.urls import path

from cart.views.add_to_cart_view import AddUpdateDeleteCartView
from order.views.place_order import PlaceOrderView

urlpatterns = [
    path("place_order", PlaceOrderView.as_view(), name="Place-Order"),
]
