from django.test import TestCase
from django.db import transaction
from warmify_core.models import User, IotDevice, Ping, Notification
from warmify_core.tasks import check_heater_is_working
from datetime import datetime, timezone, timedelta


class TasksTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="12345")
        device = IotDevice.objects.create(owner=self.user)
        self.device = device

    def tearDown(self):
        Ping.objects.all().delete()
        Notification.objects.all().delete()

    def test_notification_is_sent_if_temperature_no_change(self):
        Ping.objects.create(
            device=self.device, is_on_heater=False, recorded_heater_temperature=0
        )
        Ping.objects.create(
            device=self.device, is_on_heater=True, recorded_heater_temperature=0
        )
        Ping.objects.create(
            device=self.device, is_on_heater=True, recorded_heater_temperature=0
        )
        check_heater_is_working(self.device)
        last_notification = (
            Notification.objects.filter(device=self.device)
            .order_by("-timestamp")
            .first()
        )

        self.assertTrue(last_notification != None)

    def test_notification_not_sent_if_temperature_changes(self):
        Ping.objects.create(
            device=self.device, is_on_heater=False, recorded_heater_temperature=0
        )
        Ping.objects.create(
            device=self.device, is_on_heater=True, recorded_heater_temperature=0
        )
        Ping.objects.create(
            device=self.device, is_on_heater=True, recorded_heater_temperature=30
        )
        check_heater_is_working(self.device)
        last_notification = (
            Notification.objects.filter(device=self.device)
            .order_by("-timestamp")
            .first()
        )
        self.assertTrue(last_notification == None)

    def test_notification_not_sent_if_not_on(self):
        Ping.objects.create(
            device=self.device, is_on_heater=False, recorded_heater_temperature=0
        )
        Ping.objects.create(
            device=self.device, is_on_heater=False, recorded_heater_temperature=20
        )
        Ping.objects.create(
            device=self.device, is_on_heater=False, recorded_heater_temperature=50
        )
        check_heater_is_working(self.device.id)
        last_notification = (
            Notification.objects.filter(device=self.device)
            .order_by("-timestamp")
            .first()
        )
        self.assertTrue(last_notification == None)

    def test_notification_not_sent_if_already_on(self):
        Ping.objects.create(
            device=self.device, is_on_heater=True, recorded_heater_temperature=0
        )
        Ping.objects.create(
            device=self.device, is_on_heater=True, recorded_heater_temperature=20
        )
        check_heater_is_working(self.device)
        last_notification = (
            Notification.objects.filter(device=self.device)
            .order_by("-timestamp")
            .first()
        )
        self.assertTrue(last_notification == None)
