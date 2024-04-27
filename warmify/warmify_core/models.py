from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import uuid
from datetime import datetime, time, timezone


SIX_MINUTES_IN_SECONDS = 60 * 6


class User(AbstractUser):
    def get_device(self):
        try:
            return IotDevice.objects.get(owner=self.id)
        except IotDevice.DoesNotExist:
            return None


class IotDevice(models.Model):
    metadata = models.JSONField(default=dict, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(unique=True, default=uuid.uuid4)

    def __str__(self):
        return "{}'s device".format(self.owner.username)

    def get_events(self):
        return Event.objects.filter(device=self.id).order_by("timestamp")

    def is_active(self):
        ordered_pings = Ping.objects.filter(device=self.id).order_by("timestamp")
        if not ordered_pings:
            return False
        last_ping = ordered_pings.last()
        current_date = datetime.now(timezone.utc)
        diff = current_date - last_ping.timestamp
        return diff.seconds < SIX_MINUTES_IN_SECONDS


class Event(models.Model):
    timestamp = models.DateTimeField("event timestamp")
    metadata = models.JSONField(blank=True, null=True)
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


class ScheduleInterval(models.Model):
    start_time = models.DateTimeField("start time")
    end_time = models.DateTimeField("end time")
    metadata = models.JSONField()
    device = models.ForeignKey(IotDevice, on_delete=models.CASCADE)


class Schedule(models.Model):
    date = models.DateField("Schedule date")
    day_schedule = models.JSONField()
    device = models.ForeignKey(IotDevice, on_delete=models.CASCADE)


class Temperature(models.Model):
    value = models.FloatField("temperature value")
    timestamp = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey(IotDevice, on_delete=models.CASCADE)


class Ping(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    recorded_device_temperature = models.IntegerField(null=True)
    recorded_controller_temperature = models.IntegerField(null=True)
    recorded_waterlevel = models.IntegerField(null=True)
    device = models.ForeignKey(IotDevice, on_delete=models.CASCADE)

    @classmethod
    def get_uptime(cls):
        pass

    @classmethod
    def get_availability_today(cls):
        pass

    @classmethod
    def get_last_ping(cls, device_id):
        return cls.objects.filter(device=device_id).order_by("-timestamp").first()


NOTIFICATION_STATUS_CHOICES = {
    "success": "SUCCESS",
    "info": "INFO",
    "warning": "WARNING",
    "danger": "DANGER",
}


class Notification(models.Model):
    title = models.TextField()
    body = models.TextField()
    device = models.ForeignKey(IotDevice, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        default="info", choices=NOTIFICATION_STATUS_CHOICES, max_length=20
    )

    def __str__(self):
        return self.title[:15]

    @classmethod
    def get_unread(cls, device_id):
        return cls.objects.filter(device=device_id).filter(is_read=False)

    def mark_as_read(self):
        self.is_read = True
        self.save()
