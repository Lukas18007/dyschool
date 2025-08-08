from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for the User model
    """
    model = User
    
    # Fields to display in the list view
    list_display = [
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'user_type', 
        'is_active', 
        'date_joined'
    ]
    
    # Fields to filter by
    list_filter = [
        'user_type', 
        'is_active', 
        'is_staff', 
        'is_superuser', 
        'date_joined'
    ]
    
    # Fields to search by
    search_fields = [
        'username', 
        'email', 
        'first_name', 
        'last_name'
    ]
    
    # Fields to order by
    ordering = ['-date_joined']
    
    # Fieldsets for the edit form
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': (
                'first_name', 
                'last_name', 
                'email', 
                'user_type',
                'phone_number',
                'profile_picture',
                'bio',
                'date_of_birth',
                'address'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # Fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 
                'email', 
                'password1', 
                'password2', 
                'user_type',
                'first_name',
                'last_name'
            ),
        }),
    )
    
    # Read-only fields
    readonly_fields = ['date_joined', 'last_login']
