from django.test import TestCase
from warmify_core.models import User, IotDevice, Ping
from datetime import datetime, timezone, timedelta


class IotDeviceModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="12345")
        device = IotDevice.objects.create(owner=self.user)
        self.device = device

    def tearDown(self):
        Ping.objects.all().delete()

    def test_device_active(self):
        Ping.objects.create(device=self.device)
        self.assertEqual(self.device.is_active(), True)

    def test_device_inactive(self):
        date_minus_7_minutes = datetime.now(timezone.utc) - timedelta(
            hours=0, minutes=7
        )
        Ping.objects.create(device=self.device, timestamp=date_minus_7_minutes)
        self.assertEqual(self.device.is_active(), False)

    def test_device_inactive_no_pings(self):
        self.assertEqual(self.device.is_active(), False)
