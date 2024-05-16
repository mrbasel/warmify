from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from warmify_core.models import Event, IotDevice, Notification
from warmify_dashboard.services import fetch_dashboard_stats
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from warmify_core.utils import get_current_date, get_date_start
from warmify_core.schedules import get_schedule, schedule_to_string
from django.utils.timezone import localtime


@login_required
def index(request):
    day_range = request.GET.get("range", "1")
    users_device = IotDevice.objects.filter(owner=request.user.id)
    if not users_device:
        return redirect("no_device")
    device = users_device.first()
    schedule = get_schedule(device.id)
    context = {
        **fetch_dashboard_stats(device, int(day_range)),
        "notifications": request.notifications,
        "schedule": schedule_to_string(schedule),
        "day_range": day_range,
        "button_string": (
            "Disable heater" if device.is_enabled_heater else "Turn on heater"
        ),
    }
    return render(request, "warmify_dashboard/index.html", context)


@login_required
def events(request):
    date = request.GET.get("date", "")
    users_device = IotDevice.objects.filter(owner=request.user.id)
    if not users_device:
        return redirect("no_device")

    context = {
        "date": date if date else datetime.now().strftime("%Y-%m-%d"),
        "notifications": request.notifications,
    }
    return render(request, "warmify_dashboard/events.html", context)


@login_required
def get_events_range(request):
    day_range = int(request.GET.get("range", "1"))
    users_device = IotDevice.objects.filter(owner=request.user.id)
    if not users_device:
        return redirect("no_device")
    device = users_device.first()

    current_date = get_current_date()
    events = None
    if day_range == 7:
        target_date = current_date - timedelta(days=7)
        events = Event.objects.filter(device=device).filter(
            timestamp__gte=get_date_start(target_date)
        )
    elif day_range == 30:
        target_date = current_date - timedelta(days=30)
        events = Event.objects.filter(device=device).filter(
            timestamp__gte=get_date_start(target_date)
        )
    else:
        events = Event.get_todays_events(device.id)

    for e in events:
        e.timestamp = localtime(e.timestamp)
    events_count_by_hour = Event.get_events_count_by_hour(events)
    return JsonResponse({"events": events_count_by_hour})


@login_required
def get_events_date(request):
    current_date = get_current_date()
    date_str = request.GET.get("date", current_date.strftime("%Y-%m-%d"))
    users_device = IotDevice.objects.filter(owner=request.user.id)
    if not users_device:
        return redirect("no_device")
    device = users_device.first()

    target_date = (
        datetime.strptime(date_str, "%Y-%m-%d") if date_str else get_current_date()
    )
    events = Event.objects.filter(
        device=device,
        timestamp__year=target_date.year,
        timestamp__month=target_date.month,
        timestamp__day=target_date.day,
    )
    for e in events:
        e.timestamp = localtime(e.timestamp)
    events_count_by_hour = Event.get_events_count_by_hour(events)
    return JsonResponse({"events": events_count_by_hour})


@login_required
def reports(request):
    context = {"notifications": request.notifications}
    return render(request, "warmify_dashboard/reports.html", context=context)


@login_required
def status(request):
    context = {"notifications": request.notifications}
    return render(request, "warmify_dashboard/status.html", context=context)


@login_required
def notifications(request):
    device = request.user.get_device()
    all_notifications = Notification.objects.filter(device=device)
    read_notifications = all_notifications.filter(is_read=True)
    unread_notifications = all_notifications.filter(is_read=False)
    context = {
        "notifications": request.notifications,
        "read_notifications": read_notifications,
        "unread_notifications": unread_notifications,
    }
    return render(request, "warmify_dashboard/notifications.html", context=context)


@login_required
def mark_read(request):
    next_page = request.POST.get("next", "/")
    Notification.mark_notifications_as_read(request.user.get_device())
    context = {
        "notifications": [],
    }
    return render(
        request,
        "warmify_dashboard/components/notifications-dropdown.html",
        context=context,
    )


@login_required
def no_device(request):
    return render(request, "warmify_dashboard/no_device.html")


@login_required
def settings(request):
    context = {"notifications": request.notifications}
    return render(request, "warmify_dashboard/settings.html", context=context)


@login_required
def toggle_heater_state(request):
    device = request.user.get_device()
    device.is_enabled_heater = not device.is_enabled_heater
    device.save()
    context = {
        "button_string": (
            "Disable heater" if device.is_enabled_heater else "Enable heater"
        )
    }
    return render(
        request,
        "warmify_dashboard/components/toggle-heater-button.html",
        context=context,
    )
