from datetime import datetime, timezone, time


def human_readable_timedelta(date):
    current_date = datetime.now(timezone.utc)
    diff = current_date - date

    if diff.days >= 7:
        return f"{diff.days // 7} weeks ago"
    if diff.days >= 1:
        return f"{diff.days} days ago"
    if diff.seconds >= 3600:
        return f"{diff.seconds // 3600} hours ago"
    if diff.seconds >= 60:
        return f"{diff.seconds // 60} minutes ago"
    return "a few seconds ago"


def get_current_date():
    return datetime.now(timezone.utc)


def get_date_start(date):
    return datetime.combine(date, time.min)


def get_date_end():
    return datetime.combine(date, time.max)
