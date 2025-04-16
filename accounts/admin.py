# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, Delegate


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_full_name', 'user_type', 'company_name', 'is_verified', 'is_active')
    list_filter = ('user_type', 'is_verified', 'is_active', 'governorate')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'company_name', 'commercial_registration')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('المعلومات الشخصية'), {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        (_('المعلومات المهنية'), {'fields': ('user_type', 'company_name', 'commercial_registration', 'tax_card', 'governorate', 'address')}),
        (_('الأذونات'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('تواريخ مهمة'), {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )

    readonly_fields = ('created_at', 'updated_at')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Delegate)