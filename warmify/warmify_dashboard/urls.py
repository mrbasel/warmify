from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get_events_range/", views.get_events_range, name="get_events"),
    path("get_events_date/", views.get_events_date, name="get_events_date"),
    path("reports/", views.reports, name="reports"),
    path("events/", views.events, name="events"),
    path("status/", views.status, name="status"),
    path("settings/", views.settings, name="settings"),
    path("notifications/", views.notifications, name="notifications"),
    path("mark_read/", views.mark_read, name="read_notifications"),
    path("toggle_heater/", views.toggle_heater_state, name="toggle_heater"),
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
