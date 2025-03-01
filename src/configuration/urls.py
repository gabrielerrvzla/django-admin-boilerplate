from django.urls import path

from .views import ConfigurationView

app_name = "configuration"

urlpatterns = [
    path("", ConfigurationView.as_view(), name="menu"),
]
