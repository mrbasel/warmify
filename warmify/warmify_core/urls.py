from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("ping/", views.ping, name="ping"),
    path("log/", views.log_event, name="log"),
    path("status/", views.get_heater_status, name="status"),
]
