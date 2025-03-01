from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from account.models import User
from core.generic.services import TokenService

from .forms import LoginForm, PasswordResetConfirmForm, PasswordResetForm


class LoginView(FormView):
    template_name = "authentication/form.html"
    extra_context = {"title": _("Iniciar sesión")}
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(self.request, **form.cleaned_data)
        if user:
            login(self.request, user)
            messages.success(self.request, _(f"Bienvenido(a) {user.full_name}"))
            return redirect("admin:index")

        messages.error(self.request, _("Correo electrónico o contraseña incorrectos"))
        return self.form_invalid(form)


class PasswordResetView(FormView):
    template_name = "authentication/form.html"
    extra_context = {"title": _("Restablecer contraseña")}
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(self.request, _("No se encontró un usuario con ese correo electrónico"))
            return self.form_invalid(form)

        token_service = TokenService(salt="reset-password")
        token = token_service.generate_token(user.pk, "reset-password")

        reset_url = self.request.build_absolute_uri(f"/authentication/password-reset/confirm/{token}/")
        send_mail(
            _("Restablecimiento de contraseña"),
            _(f"Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_url}"),
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )

        messages.info(self.request, _("Se ha enviado un mensaje con las instrucciones para restablecer tu contraseña"))
        return redirect("authentication:login")


class PasswordResetConfirmView(FormView):
    template_name = "authentication/form.html"
    extra_context = {"title": _("Restablecimiento de contraseña")}
    form_class = PasswordResetConfirmForm

    def dispatch(self, request, *args, **kwargs):
        token = kwargs["token"]
        token_service = TokenService(salt="reset-password")
        user_id = token_service.validate_token(token, "reset-password")
        if not user_id:
            messages.error(request, _("El enlace de restablecimiento de contraseña no es válido o ha expirado"))
            return redirect("authentication:login")

        self.user = User.objects.get(pk=user_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data["new_password2"]
        self.user.set_password(password)
        self.user.save()

        token_service = TokenService(salt="reset-password")
        token_service.invalidate_token(self.kwargs["token"])
        messages.success(self.request, _("Se ha restablecido tu contraseña correctamente"))
        return redirect("authentication:login")
