from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from warmify_core.models import Event, IotDevice
from warmify_dashboard.services import fetch_dashboard_stats
from django.core.paginator import Paginator


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
def events(request):
    user_id = request.user.id
    users_device = get_object_or_404(IotDevice, owner=user_id)
    all_events = users_device.get_events()

    paginator = Paginator(all_events, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, "warmify_dashboard/events.html", context)


@login_required
def settings(request):
    return render(request, "warmify_dashboard/settings.html")
