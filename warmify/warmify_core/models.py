from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import uuid

class User(AbstractUser):
    pass

class IotDevice(models.Model):
    metadata = models.JSONField(default=dict, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    token = models.UUIDField(unique=True, default=uuid.uuid4)

    def __str__(self):
        return "{}'s device".format(self.owner.username)

class Event(models.Model):
    timestamp = models.DateTimeField("event timestamp")
    metadata = models.JSONField(blank=True, null=True)
    device = models.ForeignKey(IotDevice, on_delete=models.CASCADE)

    def __str__(self):
        return "Event {} at {}".format(self.id, self.timestamp.strftime("%d/%m/%y, %H:%M:%S"))

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
