from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from core.generic.views import GenericFormView, GenericUpdateView

from .forms import ChangePasswordForm, ProfileForm


class ProfileView(GenericUpdateView):
    extra_context = {
        "title": _("Perfil"),
        "breadcrumbs": [
            {"label": _("Configuración"), "url": reverse_lazy("configuration")},
            {"label": _("Perfil"), "url": ""},
        ],
    }
    success_message = _("Perfil actualizado correctamente.")
    permission_required = []
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return self.request.path


class ChangePasswordView(GenericFormView):
    extra_context = {
        "title": _("Cambiar contraseña"),
        "breadcrumbs": [
            {"label": _("Configuración"), "url": reverse_lazy("configuration")},
            {"label": _("Cambiar contraseña"), "url": ""},
        ],
    }
    success_message = _("Contraseña actualizada correctamente.")
    permission_required = []
    form_class = ChangePasswordForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        user = self.request.user
        old_password = form.cleaned_data["password"]
        new_password = form.cleaned_data["confirm_password"]

        if not user.check_password(old_password):
            form.add_error("password", _("La contraseña actual no es correcta."))
            return self.form_invalid(form)

        user.set_password(new_password)
        user.save()
        return super().form_valid(form)
