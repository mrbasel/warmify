from datetime import datetime, timedelta, time, timezone
from .models import Event
from django.utils.timezone import localtime


def generate_schedule(events):
    for e in events:
        e.timestamp = localtime(e.timestamp)

    if len(events) == 0:
        return [1 for i in range(24)]

    schedule = [0 for i in range(24)]
    for e in events:
        schedule[e.timestamp.hour] = 1

    return schedule


def get_schedule(device_id):
    last_weeks_day = datetime.today() - timedelta(days=7)
    last_weeks_day_events = Event.objects.filter(
        device=device_id,
        timestamp__year=last_weeks_day.year,
        timestamp__month=last_weeks_day.month,
        timestamp__day=last_weeks_day.day,
    )

    if len(last_weeks_day_events) != 0:
        return generate_schedule(last_weeks_day_events)

    yesterday_start = datetime.today() - timedelta(days=1)
    yesterday_events = Event.objects.filter(
        device=device_id,
        timestamp__year=yesterday_start.year,
        timestamp__month=yesterday_start.month,
        timestamp__day=yesterday_start.day,
    )
    if len(yesterday_events) != 0:
        return generate_schedule(yesterday_events)

    return generate_schedule([])


# Needs refactoring..
def schedule_to_string(schedule):
    current_date = datetime.now(timezone.utc)
    to_string = lambda i: f"{'0' if i < 10 else ''}{i}:00-{i}:59"
    return [
        {
            "string": to_string(i),
            "is_active": schedule[i],
            "is_now": current_date.hour + 3 == i,
        }
        for i in range(24)
    ]
