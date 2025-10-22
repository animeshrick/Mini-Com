from django.contrib import admin
from auth_api.models.user_models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Custom Admin for our own User model.
    This version does NOT depend on Django's auth system.
    """
    list_display = ("email", "name", "account_type", "is_active", "is_deleted")
    list_filter = ("is_active", "account_type", "is_deleted")
    search_fields = ("email", "name")
    ordering = ("email",)

    fieldsets = (
        ("Basic Info", {"fields": ("email", "password", "name", "dob", "phone", "account_type")}),
        ("Address Info", {"fields": ("address", "pincode", "lat", "lan")}),
        ("Status", {"fields": ("is_active", "is_deleted")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    readonly_fields = ("created_at", "updated_at")
