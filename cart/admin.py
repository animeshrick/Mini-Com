from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ('subtotal',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    inlines = [CartItemInline]
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('product__name', 'cart__user__email')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
