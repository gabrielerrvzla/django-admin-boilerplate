from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Div, Layout, Row, Submit
from django import forms
from django.contrib.auth import password_validation
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from core.generic.forms import Link

from .models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].disabled = True

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    HTML(f'<h5 class="card-title">{_("Información básica")}</h5>'),
                    css_class="card-header",
                ),
                Div(
                    Row(Column("full_name")),
                    Row(Column("email")),
                    css_class="card-body",
                ),
                Div(
                    Submit("submit", _("Actualizar")),
                    Link(_("Volver"), reverse_lazy("configuration"), css_class="btn btn-outline-secondary"),
                    css_class="card-footer",
                ),
                css_class="card",
            )
        )


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        label=_("Contraseña actual"),
        widget=forms.PasswordInput,
    )

    new_password = forms.CharField(
        label=_("Nueva contraseña"),
        widget=forms.PasswordInput,
    )

    confirm_password = forms.CharField(
        label=_("Confirmar nueva contraseña"),
        widget=forms.PasswordInput,
        validators=[password_validation.validate_password],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    HTML(f'<h5 class="card-title">{_("Cambiar contraseña")}</h5>'),
                    css_class="card-header",
                ),
                Div(
                    Row(Column("password")),
                    Row(Column("new_password")),
                    Row(Column("confirm_password")),
                    css_class="card-body",
                ),
                Div(
                    Submit("submit", _("Actualizar")),
                    Link(_("Volver"), reverse_lazy("configuration"), css_class="btn btn-outline-secondary"),
                    css_class="card-footer",
                ),
                css_class="card",
            )
        )

    def clean(self):
        cleaned_data = super().clean()

        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error("confirm_password", _("Las contraseñas no coinciden"))

        return cleaned_data


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput,
        validators=[password_validation.validate_password],
    )

    class Meta:
        model = User
        fields = ["full_name", "email", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Row(Column("full_name")),
                    Row(Column("email")),
                    Row(Column("password")),
                    css_class="card-body",
                ),
                Div(
                    Submit("submit", _("Crear")),
                    Link(_("Volver"), reverse_lazy("user-list"), css_class="btn btn-outline-secondary"),
                    css_class="card-footer",
                ),
                css_class="card",
            )
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name", "email", "is_active", "groups"]
        widgets = {
            "is_active": forms.Select(choices=((True, _("Activo")), (False, _("Inactivo")))),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Row(Column("full_name")),
                    Row(Column("email")),
                    Row(Column("is_active")),
                    Row(Column("groups")),
                    css_class="card-body",
                ),
                Div(
                    Submit("submit", _("Actualizar")),
                    Link(_("Volver"), reverse_lazy("user-list"), css_class="btn btn-outline-secondary"),
                    css_class="card-footer",
                ),
                css_class="card",
            )
        )
