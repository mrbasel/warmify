from django.db import models
from .device import IotDevice


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
