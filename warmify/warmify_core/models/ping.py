from django.db import models
from .device import IotDevice
from datetime import datetime


class Ping(models.Model):
    timestamp = models.DateTimeField(default=datetime.now)
    recorded_heater_temperature = models.IntegerField(null=True)
    recorded_controller_temperature = models.IntegerField(null=True)
    recorded_waterlevel = models.IntegerField(null=True)
    is_on_heater = models.BooleanField(null=True)
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
