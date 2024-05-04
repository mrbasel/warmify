from django.test import TestCase, Client
from warmify_core.models import User, IotDevice

username = "test"
password = "12345"


class DashboardViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=username, password=password)
        self.device = IotDevice.objects.create(owner=self.user)
        self.client = Client()

    def tearDown(self):
        pass

    def test_login_correct_credentials(self):
        is_successful = self.client.login(username=username, password=password)
        self.assertEqual(is_successful, True)

    def test_login_incorrect_credentials(self):
        is_successful = self.client.login(username=username, password="111111")
        self.assertEqual(is_successful, False)

    def test_logout(self):
        pass

    def test_index(self):
        self.client.login(username=username, password=password)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)

    def test_index_no_auth(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_events(self):
        self.client.login(username=username, password=password)
        response = self.client.get("/events/")
        self.assertEqual(response.status_code, 200)

    def test_events_no_auth(self):
        response = self.client.get("/events/")
        self.assertEqual(response.status_code, 302)

    def test_notifications(self):
        self.client.login(username=username, password=password)
        response = self.client.get("/notifications/")
        self.assertEqual(response.status_code, 200)

    def test_notifications_no_auth(self):
        response = self.client.get("/notifications/")
        self.assertEqual(response.status_code, 302)
