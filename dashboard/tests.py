from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class DashboardAndCrudSmokeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="secret123")

    def test_login_page_renders(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_renders_for_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SOC Operations Dashboard")

    def test_incident_create_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("incident_create"))
        self.assertEqual(response.status_code, 200)
