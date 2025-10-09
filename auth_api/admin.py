from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    """
    Custom UserAdmin for the custom User model.
    """
    # Fields to display in the user list
    list_display = ('email', 'username', 'name', 'is_active', 'account_type')
    # Filters available on the right sidebar
    list_filter = ('is_active', 'account_type', 'is_deleted')
    # Fields to search by
    search_fields = ('email', 'username', 'name')
    ordering = ('email',)

    # This is crucial. The default UserAdmin expects 'groups' and 'user_permissions'.
    # We set it to an empty tuple because our custom user model doesn't have them.
    filter_horizontal = ()

    # Customize the fields displayed on the user edit page.
    # We override the default fieldsets to match our model.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'name', 'dob', 'phone', 'address', 'pincode')}),
        ('Permissions', {'fields': ('is_active', 'is_deleted', 'account_type')}),
        ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )

    # Customize the fields on the user creation page.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password'),
        }),
    )

    # Make date fields read-only in the admin
    readonly_fields = ('created_at', 'updated_at')

# Register the User model with our custom UserAdmin
admin.site.register(User, UserAdmin)
