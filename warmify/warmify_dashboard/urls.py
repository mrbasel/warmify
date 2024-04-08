from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("reports/", views.reports, name="reports"),
    path("logs/", views.logs, name="logs"),
    path("settings/", views.settings, name="settings"),
]
