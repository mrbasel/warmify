from warmify_core.models import Event, Ping
from warmify_core.schedules import get_schedule
from warmify_dashboard.utils import human_readable_timedelta
from math import floor
from warmify_dashboard.utils import get_current_date, get_date_start, get_date_end
from datetime import timedelta


def fetch_dashboard_stats(device, day_range=1):
    device_id = device.id
    events = None
    current_date = get_current_date()
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
        events = Event.get_todays_events(device_id)

    schedule = get_schedule(device_id)
    saving_percentage = floor(schedule.count(0) / (day_range * 24 * 100))

    events_count_by_hour = Event.get_events_count_by_hour(events)
    if sum(events_count_by_hour) == 0:
        most_active_time_string = "-"
    else:
        most_active_time = events_count_by_hour.index(max(events_count_by_hour))
        most_active_time_string = f"{most_active_time}:00-{most_active_time+1}:00"

    is_up = device.is_active()
    last_ping = Ping.get_last_ping(device_id)
    if last_ping:
        last_ping_timedelta = human_readable_timedelta(last_ping.timestamp)
    else:
        last_ping_timedelta = "-"

    data = {
        "events_count": events.count(),
        "saving_percentage": saving_percentage,
        "active_time": most_active_time_string,
        "water_usage": 30,
        "events_count_by_hour": events_count_by_hour,
        "is_up": is_up,
        "last_ping": last_ping_timedelta,
    }
    return data
