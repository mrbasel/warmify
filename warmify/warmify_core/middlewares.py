from .models import Notification


class NotificationsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            device = request.user.get_device()
            if device:
                request.notifications = Notification.get_unread(device.id)
        response = self.get_response(request)
        return response
