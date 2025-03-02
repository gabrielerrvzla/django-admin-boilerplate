from django.urls import path

from .views import (
    ChangePasswordView,
    ProfileView,
    UserCreateView,
    UserDeleteView,
    UserExportView,
    UserListView,
    UserUpdateView,
)

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/create/", UserCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user-delete"),
    path("users/export/", UserExportView.as_view(), name="user-export"),
]
