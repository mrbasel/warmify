from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("reports/", views.reports, name="reports"),
    path("get_events/", views.get_events, name="get_events"),
    path("events/", views.events, name="events"),
    path("settings/", views.settings, name="settings"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            redirect_authenticated_user=True,
            template_name="warmify_dashboard/login.html",
            next_page="index",
        ),
        name="login",
    ),
]
