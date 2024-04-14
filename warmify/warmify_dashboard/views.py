from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from warmify_core.models import Event, IotDevice
from warmify_dashboard.services import fetch_dashboard_stats


@login_required
def index(request):
    user_id = request.user.id
    users_device = get_object_or_404(IotDevice, owner=user_id)
    context = fetch_dashboard_stats(users_device.id)
    return render(request, "warmify_dashboard/index.html", context)


@login_required
def get_events(request):
    user_id = request.user.id
    users_device = get_object_or_404(IotDevice, owner=user_id)
    data = fetch_dashboard_stats(users_device.id)
    return JsonResponse({"events": data["events_count_by_hour"]})


@login_required
def reports(request):
    return render(request, "warmify_dashboard/reports.html")


@login_required
def logs(request):
    return render(request, "warmify_dashboard/logs.html")


@login_required
def settings(request):
    return render(request, "warmify_dashboard/settings.html")
