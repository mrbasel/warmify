from warmify_core.events import get_events_count_by_hour
from warmify_core.models import Event, Ping
from warmify_core.schedules import get_schedule
from warmify_dashboard.utils import human_readable_timedelta
from math import floor


def fetch_dashboard_stats(device):
    device_id = device.id
    todays_events = Event.get_todays_events(device_id)

    schedule = get_schedule(device_id)
    saving_percentage = floor(schedule.count(0) / 24 * 100)

    events_count_by_hour = get_events_count_by_hour(todays_events)
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
        "events_count": todays_events.count(),
        "saving_percentage": saving_percentage,
        "active_time": most_active_time_string,
        "water_usage": 30,
        "events_count_by_hour": events_count_by_hour,
        "is_up": is_up,
        "last_ping": last_ping_timedelta,
    }
    return data
