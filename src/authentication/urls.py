from django.urls import path

from .views import LoginView, LogoutView, PasswordResetConfirmView, PasswordResetView

app_name = "authentication"

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
    path("password-reset/confirm/<token>/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
]
