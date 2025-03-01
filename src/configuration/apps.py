from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ConfigurationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "configuration"
    verbose_name = _("Configuración")
