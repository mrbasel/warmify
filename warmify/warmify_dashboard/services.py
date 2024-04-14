from datetime import datetime, time
from warmify_core.models import Event
from warmify_core.utils import get_schedule
from math import floor


def fetch_dashboard_stats(device_id):
    today = datetime.today()
    today_start = datetime.combine(today, time.min)
    today_end = datetime.combine(today, time.max)
    todays_events = (
        Event.objects.filter(device=device_id)
        .filter(timestamp__gte=today_start)
        .filter(timestamp__lte=today_end)
    )

    schedule = get_schedule(device_id)
    saving_percentage = floor(schedule.count(0) / 24 * 100)

    events_count_by_hour = get_events_count_by_hour(todays_events)
    if sum(events_count_by_hour) == 0:
        most_active_time_string = "-"
    else:
        most_active_time = events_count_by_hour.index(max(events_count_by_hour))
        most_active_time_string = f"{most_active_time}:00-{most_active_time+1}:00"

    data = {
        "events_count": todays_events.count(),
        "saving_percentage": saving_percentage,
        "active_time": most_active_time_string,
        "water_usage": 30,
        "events_count_by_hour": events_count_by_hour,
    }
    return data


def get_events_count_by_hour(events):
    events_count = [0 for _ in range(24)]
    for e in events:
        events_count[e.timestamp.hour] += 1
    return events_count
