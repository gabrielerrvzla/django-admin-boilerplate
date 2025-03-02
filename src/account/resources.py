from django.utils.translation import gettext_lazy as _
from import_export import fields, resources

from .models import User


class UserResource(resources.ModelResource):
    full_name = fields.Field(
        attribute="full_name",
        column_name=_("Nombre"),
    )

    email = fields.Field(
        attribute="email",
        column_name=_("Correo electrónico"),
    )

    is_active = fields.Field(
        attribute="is_active",
        column_name=_("Activo"),
    )

    class Meta:
        model = User
        fields = ("full_name", "email", "is_active")
        export_order = fields

    def dehydrate_is_active(self, user: User) -> str:
        return "Si" if user.is_active else "No"
