from django.db import models, transaction
from .device import IotDevice

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

    @classmethod
    def mark_notifications_as_read(cls, device_id):
        unread_notifications = cls.objects.filter(device=device_id).filter(
            is_read=False
        )
        with transaction.atomic():
            try:
                for notification in unread_notifications:
                    notification.is_read = True
                    notification.save()
                return True
            except IntegrityError:
                return False

    def mark_as_read(self):
        self.is_read = True
        self.save()
