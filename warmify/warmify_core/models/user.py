from django.contrib.auth.models import AbstractUser
from .device import IotDevice


class User(AbstractUser):
    def get_device(self):
        try:
            return IotDevice.objects.get(owner=self.id)
        except IotDevice.DoesNotExist:
            return None
