from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from warmify_core.models import Event, IotDevice
from warmify_dashboard.services import fetch_dashboard_stats
from django.core.paginator import Paginator


@login_required
def index(request):
    users_device = IotDevice.objects.filter(owner=request.user.id)
    if not users_device:
        return redirect("no_device")
    context = fetch_dashboard_stats(users_device.first())
    return render(request, "warmify_dashboard/index.html", context)


@login_required
def get_events(request):
    users_device = IotDevice.objects.filter(owner=request.user.id)
    if not users_device:
        return redirect("no_device")
    device = users_device.first()
    events_count_by_hour = Event.get_events_count_by_hour(
        Event.get_todays_events(device.id)
    )
    return JsonResponse({"events": events_count_by_hour})


@login_required
def reports(request):
    return render(request, "warmify_dashboard/reports.html")


@login_required
def status(request):
    return render(request, "warmify_dashboard/status.html")


@login_required
def no_device(request):
    return render(request, "warmify_dashboard/no_device.html")


@login_required
def events(request):
    users_device = IotDevice.objects.filter(owner=request.user.id)
    if not users_device:
        return redirect("no_device")
    all_events = users_device.first().get_events()

    paginator = Paginator(all_events, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    range = list(paginator.get_elided_page_range(page_number if page_number else 1))

    context = {"page_obj": page_obj, "range": range}
    return render(request, "warmify_dashboard/events.html", context)


@login_required
def settings(request):
    return render(request, "warmify_dashboard/settings.html")
