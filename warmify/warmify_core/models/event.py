from django.db import models
from .device import IotDevice
from datetime import datetime, time, timezone


def default_datetime():
    return datetime.now()


class Event(models.Model):
    timestamp = models.DateTimeField("event timestamp", default=default_datetime)
    usage_milliliters = models.IntegerField(
        "Usage in milliliters", null=True, blank=True
    )
    device = models.ForeignKey(IotDevice, on_delete=models.CASCADE)

    def __str__(self):
        return "Event {} at {}".format(
            self.id, self.timestamp.strftime("%d/%m/%y, %H:%M:%S")
        )

    @classmethod
    def get_todays_events(cls, device_id):
        today = datetime.now(timezone.utc)
        today_start = datetime.combine(today, time.min)
        today_end = datetime.combine(today, time.max)
        return (
            cls.objects.filter(device=device_id)
            .filter(timestamp__gte=today_start)
            .filter(timestamp__lte=today_end)
        )

    @classmethod
    def get_todays_usage(cls, device_id):
        """Return today's total water usage in liters"""
        today = datetime.now()
        today_start = datetime.combine(today, time.min)
        today_end = datetime.combine(today, time.max)
        filtered_query = (
            cls.objects.filter(device=device_id)
            .filter(timestamp__gte=today_start)
            .filter(timestamp__lte=today_end)
        )

        total_usage = 0
        for i in filtered_query:
            total_usage += i.usage_milliliters
        return total_usage / 1000

    @classmethod
    def get_events_count_by_hour(cls, events):
        events_count = [0 for _ in range(24)]
        for e in events:
            events_count[e.timestamp.hour] += 1
        return events_count

    @property
    def readable_date(self):
        return self.timestamp.strftime("%d/%m/%y")

    @property
    def readable_time(self):
        return self.timestamp.strftime("%H:%M:%S")
