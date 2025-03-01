from django.urls import path

from .views import LoginView, PasswordResetConfirmView, PasswordResetView

app_name = "authentication"

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
    path("password-reset/confirm/<token>/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
]
