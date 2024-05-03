from celery import shared_task
from warmify_core.models import Ping, Notification


@shared_task
def check_heater_is_working(device_id):
    last_five_pings = list(Ping.objects.filter(device=device_id).order_by("-id")[:5])
    if not last_five_pings:
        return
    last_ping = last_five_pings[0]
    target_ping = None
    try:
        for ping in last_five_pings:
            if not ping.is_on_heater:
                target_ping = last_five_pings[last_five_pings.index(ping) - 1]
                break
    except (IndexError, ValueError):
        return

    if not target_ping:
        return

    print("last_ping:", last_ping)
    print("target_ping:", target_ping)
    temperature_difference = (
        last_ping.recorded_heater_temperature - target_ping.recorded_heater_temperature
    )

    if temperature_difference < 5:
        Notification.objects.create(
            device=device_id,
            title="Heater alert!",
            body="Your heater is not functioning properly.",
            status="danger",
        )
