from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, FormView, UpdateView


class GenericFormView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "generic/form.html"
    success_message = _("Acción realizada correctamente.")


class GenericCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "generic/form.html"
    success_message = _("Acción realizada correctamente.")


class GenericUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "generic/form.html"
    success_message = _("Acción realizada correctamente.")
