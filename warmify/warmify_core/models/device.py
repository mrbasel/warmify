from django.db import models
from django.conf import settings
import uuid
from datetime import datetime, timezone

SIX_MINUTES_IN_SECONDS = 60 * 6


class IotDevice(models.Model):
    metadata = models.JSONField(default=dict, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(unique=True, default=uuid.uuid4)

    def __str__(self):
        return "{}'s device".format(self.owner.username)

    def get_events(self):
        from .event import Event

        return Event.objects.filter(device=self.id).order_by("timestamp")

    def is_active(self):
        from .ping import Ping

        ordered_pings = Ping.objects.filter(device=self.id).order_by("id")
        if not ordered_pings:
            return False
        last_ping = ordered_pings.last()
        current_date = datetime.now(timezone.utc)
        diff = current_date - last_ping.timestamp
        return diff.seconds < SIX_MINUTES_IN_SECONDS
