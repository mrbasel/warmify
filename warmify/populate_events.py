import os
from datetime import datetime
from random import randint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "warmify.settings")
import django

django.setup()
from warmify_core.models import Event

today = datetime.today()
for i in range(50):
    timestamp = datetime(
        today.year, today.month, today.day, randint(6, 20), randint(0, 59)
    )
    Event.objects.create(
        device_id=1, timestamp=timestamp, usage_milliliters=randint(10, 1000)
    )
