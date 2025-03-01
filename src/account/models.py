from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.generic.models import TimeStampedModel

from .managers import UserManager


class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(
        max_length=255,
        verbose_name=_("Nombre completo"),
    )

    email = models.EmailField(
        unique=True,
        verbose_name=_("Correo electrónico"),
    )

    password = models.CharField(
        max_length=128,
        verbose_name=_("Contraseña"),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("¿Activo?"),
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name=_("¿Es staff?"),
        help_text=_("Designa si el usuario puede acceder al sitio de administración."),
    )

    is_superuser = models.BooleanField(
        default=False,
        verbose_name=_("¿Es superusuario?"),
        help_text=_("Designa si el usuario tiene todos los permisos sin asignarlos explícitamente."),
    )

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")
        ordering = ["-created_at"]
        default_permissions = []
        permissions = [
            ("view_user", _("Ver usuario")),
            ("add_user", _("Agregar usuario")),
            ("update_user", _("Actualizar usuario")),
            ("delete_user", _("Eliminar usuario")),
        ]

    def __str__(self):
        return self.email
