from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from core.generic.views import (
    GenericCreateView,
    GenericDeleteView,
    GenericExportView,
    GenericFormView,
    GenericListView,
    GenericUpdateView,
)

from .filtersets import UserFilterset
from .forms import ChangePasswordForm, ProfileForm, UserCreateForm, UserUpdateForm
from .models import User
from .resources import UserResource


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


class UserListView(GenericListView):
    model = User
    filterset = UserFilterset
    permission_required = "account.view_user"
    extra_context = {
        "title": _("Usuarios"),
        "breadcrumbs": [
            {"label": _("Usuarios"), "url": ""},
        ],
    }
    actions = [
        {
            "url": reverse_lazy("user-create"),
            "permission": "account.add_user",
            "label": _("Crear usuario"),
            "method": "GET",
        },
        {
            "url": reverse_lazy("user-export"),
            "permission": "account.view_user",
            "label": _("Exportar"),
            "method": "POST",
        },
    ]
    columns = [
        {
            "name": _("Nombre"),
            "field": "full_name",
        },
        {
            "name": _("Correo electrónico"),
            "field": "email",
        },
    ]
    columns_actions = [
        {
            "url": lambda obj: reverse_lazy("user-update", kwargs={"pk": obj.pk}),
            "style": "warning",
            "icon": "bi bi-pencil",
            "tooltip": _("Actualizar"),
            "permission": "account.update_user",
            "method": "GET",
        },
        {
            "url": lambda obj: reverse_lazy("user-delete", kwargs={"pk": obj.pk}),
            "style": "danger",
            "icon": "bi bi-trash",
            "tooltip": _("Eliminar"),
            "permission": "account.delete_user",
            "method": "GET",
        },
    ]

    def get_queryset(self):
        return (
            super().get_queryset().filter(is_superuser=False).exclude(pk=self.request.user.pk).order_by("-created_at")
        )


class UserCreateView(GenericCreateView):
    model = User
    form_class = UserCreateForm
    permission_required = "account.add_user"
    success_message = _("Usuario creado correctamente.")
    extra_context = {
        "title": _("Crear usuario"),
        "breadcrumbs": [
            {"label": _("Usuarios"), "url": reverse_lazy("user-list")},
            {"label": _("Crear usuario"), "url": ""},
        ],
    }

    def get_success_url(self):
        return reverse_lazy("user-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)


class UserUpdateView(GenericUpdateView):
    model = User
    form_class = UserUpdateForm
    permission_required = "account.update_user"
    success_message = _("Usuario actualizado correctamente.")
    extra_context = {
        "title": _("Actualizar usuario"),
        "breadcrumbs": [
            {"label": _("Usuarios"), "url": reverse_lazy("user-list")},
            {"label": _("Actualizar usuario"), "url": ""},
        ],
    }

    def get_success_url(self):
        return reverse_lazy("user-list")

    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=False).exclude(pk=self.request.user.pk)


class UserDeleteView(GenericDeleteView):
    model = User
    permission_required = "account.delete_user"
    success_message = _("Usuario eliminado correctamente.")
    extra_context = {
        "title": _("Eliminar usuario"),
        "back_url": reverse_lazy("user-list"),
        "breadcrumbs": [
            {"label": _("Usuarios"), "url": reverse_lazy("user-list")},
            {"label": _("Eliminar usuario"), "url": ""},
        ],
    }

    def get_success_url(self):
        return reverse_lazy("user-list")

    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=False).exclude(pk=self.request.user.pk)


class UserExportView(GenericExportView):
    format = "xlsx"
    filterset = UserFilterset
    permission_required = "account.view_user"
    resource_class = UserResource

    def get_queryset(self):
        return (
            super().get_queryset().filter(is_superuser=False).exclude(pk=self.request.user.pk).order_by("-created_at")
        )
