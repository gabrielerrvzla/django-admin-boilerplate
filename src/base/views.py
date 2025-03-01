from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "base/home.html"
    extra_context = {
        "title": _("Inicio"),
        "breadcrumbs": [
            {"label": _("Inicio"), "url": ""},
        ],
    }


class ConfigurationView(LoginRequiredMixin, TemplateView):
    template_name = "base/configuration.html"
    extra_context = {
        "title": _("Configuración"),
        "breadcrumbs": [
            {"label": _("Configuración"), "url": ""},
        ],
    }
    menu = [
        {
            "label": _("Cuenta"),
            "children": [
                {
                    "label": _("Perfil"),
                    "url": "#",
                },
                {
                    "label": _("Cambiar contraseña"),
                    "url": "#",
                },
                {
                    "label": _("Cerrar sesión"),
                    "url": reverse_lazy("logout"),
                },
            ],
        },
        {
            "label": _("Administración"),
            "children": [
                {
                    "label": _("Usuarios"),
                    "url": "#",
                    "permission": "user.view_user",
                },
            ],
        },
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["configuration_menu"] = self._process_menu(self.menu)
        return context

    def _process_menu(self, menu):
        process_menu = []

        for item in menu:
            if "permission" in item and not self.request.user.has_perm(item["permission"]):
                continue

            if "children" in item:
                children = self._process_menu(item["children"])
                if not children:
                    continue
                item["children"] = children

            process_menu.append(item)

        return process_menu
