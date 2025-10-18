from django.contrib import admin
from order.models.order import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at', 'order_status']
    list_filter = ['order_status', 'created_at', 'updated_at']
    search_fields = ['user__username', 'id']
