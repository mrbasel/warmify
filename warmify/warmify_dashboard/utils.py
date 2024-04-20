from datetime import datetime, timezone


def human_readable_timedelta(date):
    current_date = datetime.now(timezone.utc)
    diff = current_date - date

    if diff.days >= 7:
        return f"{diff.days // 7} weeks ago"
    if diff.days >= 1:
        return f"{diff.days} days ago"
    if diff.seconds >= 60:
        return f"{diff.seconds // 60} minutes ago"
    return "a few seconds ago"
