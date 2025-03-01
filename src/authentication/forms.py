from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Div, Layout, Row, Submit
from django import forms
from django.contrib.auth import password_validation
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={"autofocus": True}),
    )

    password = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Row(Column("email")),
                    Row(Column("password")),
                    Row(Column(Submit("submit", _("Iniciar sesión"), css_class="w-100"))),
                    css_class="card-body login-card-body",
                ),
                css_class="card",
            ),
            Div(
                HTML(f'<a href="{reverse_lazy("authentication:password-reset")}">{_("¿Olvidaste tu contraseña?")}</a>'),
                css_class="text-center mt-3",
            ),
        )


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={"autofocus": True}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Row(Column("email")),
                    Row(Column(Submit("submit", _("Restablecer contraseña"), css_class="w-100"))),
                    css_class="card-body login-card-body",
                ),
                css_class="card",
            ),
            Div(
                HTML(f'<a href="{reverse_lazy("authentication:login")}">{_("Iniciar sesión")}</a>'),
                css_class="text-center mt-3",
            ),
        )


class PasswordResetConfirmForm(forms.Form):
    new_password1 = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput,
    )

    new_password2 = forms.CharField(
        label=_("Confirmar contraseña"),
        widget=forms.PasswordInput,
        validators=[password_validation.validate_password],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Row(Column("new_password1")),
                    Row(Column("new_password2")),
                    Row(Column(Submit("submit", _("Restablecer contraseña"), css_class="w-100"))),
                    css_class="card-body login-card-body",
                ),
                css_class="card",
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError({"new_password2": _("Las contraseñas no coinciden")})

        return cleaned_data
