from django.urls import path

from .views import ConfigurationView, HomeView


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("configuration/", ConfigurationView.as_view(), name="configuration"),
]
