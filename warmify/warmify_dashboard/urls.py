from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("reports/", views.reports, name="reports"),
    path("get_events/", views.get_events, name="get_events"),
    path("events/", views.events, name="events"),
    path("settings/", views.settings, name="settings"),
    path("setup_incomplete/", views.no_device, name="no_device"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            redirect_authenticated_user=True,
            template_name="warmify_dashboard/login.html",
            next_page="index",
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
]
