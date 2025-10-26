from django.urls import path

from order.views.order_list import OrderListView
from order.views.place_order import PlaceOrderView

urlpatterns = [
    path("place_order", PlaceOrderView.as_view(), name="Place-Order"),
    path("user_orders", OrderListView.as_view(), name="Get-Orders"),
]
