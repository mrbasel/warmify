from celery import shared_task
from warmify_core.models import Ping, Notification, IotDevice
from datetime import datetime, timezone, time


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

    temperature_difference = (
        last_ping.recorded_heater_temperature - target_ping.recorded_heater_temperature
    )
    if temperature_difference > 5:
        device = IotDevice.objects.get(id=device_id)
        Notification.objects.create(
            device=device,
            title="Heater alert!",
            body="Your heater is not functioning properly.",
            status="danger",
            notification_type="heater_not_working",
        )


@shared_task
def alert_empty_tank(device_id):
    current_date = datetime.combine(datetime.now(timezone.utc), time.min)
    todays_empty_tank_alerts = (
        Notification.objects.filter(device=device_id)
        .filter(timestamp__gte=current_date)
        .filter(notification_type="empty_tank")
    )
    if not todays_empty_tank_alerts:
        device = IotDevice.objects.get(id=device_id)
        Notification.objects.create(
            device=device,
            title="Tank alert!",
            body="Your water tank does not have enough water.",
            status="danger",
            notification_type="empty_tank",
        )
