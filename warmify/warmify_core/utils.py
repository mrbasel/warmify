from datetime import datetime, timedelta, time
from .models import Event


def generate_schedule(events):
    if len(events) == 0:
        return [1 for i in range(24)]

    schedule = [0 for i in range(24)]
    for e in events:
        schedule[e.timestamp.hour] = 1

    return schedule


def get_schedule(device_id):
    last_weeks_day_start = datetime.combine(datetime.today(), time.min) - timedelta(
        days=7
    )
    last_weeks_day_end = datetime.combine(datetime.today(), time.max) - timedelta(
        days=7
    )
    last_weeks_day_events = Event.objects.filter(
        timestamp__gte=last_weeks_day_start
    ).filter(timestamp__lte=last_weeks_day_end)

    if len(last_weeks_day_events) != 0:
        return generate_schedule(last_weeks_day_events)

    yesterday_start = datetime.combine(datetime.today(), time.min) - timedelta(days=1)
    yesterday_end = datetime.combine(datetime.today(), time.max) - timedelta(days=1)
    yesterday_events = Event.objects.filter(timestamp__gte=yesterday_start).filter(
        timestamp__lte=yesterday_end
    )

    if len(yesterday_events) != 0:
        return generate_schedule(yesterday_events)

    return generate_schedule([])
