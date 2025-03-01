from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = [
        "-created_at",
    ]

    list_display = (
        "email",
        "is_active",
        "is_superuser",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "full_name",
        "email",
    )

    readonly_fields = (
        "pk",
        "created_at",
        "updated_at",
        "last_login",
    )

    fieldsets = (
        (
            _("Información personal"),
            {
                "fields": [
                    "full_name",
                ]
            },
        ),
        (
            _("Cuenta"),
            {
                "fields": [
                    "email",
                    "password",
                ]
            },
        ),
        (
            _("Permisos"),
            {
                "fields": [
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                    "groups",
                ]
            },
        ),
        (
            _("Auditoría"),
            {
                "fields": [
                    "created_at",
                    "updated_at",
                    "last_login",
                ]
            },
        ),
    )
