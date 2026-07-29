from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Incident, IncidentCategory, IncidentSeverity, IncidentStatus


class IncidentFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="qauser", password="secret123")

    def test_create_view_redirects_to_incidents_list_and_incident_is_visible(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("incident_create"),
            {
                "incident_id": "INC-1001",
                "title": "Suspicious login activity",
                "description": "A new test incident created through the create view.",
                "category": IncidentCategory.PHISHING,
                "severity": IncidentSeverity.HIGH,
                "status": IncidentStatus.OPEN,
                "source": "QA Test",
                "assigned_to": "",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("incidents"))

        incident = Incident.objects.get(incident_id="INC-1001")
        self.assertEqual(incident.created_by, self.user)

        list_response = self.client.get(reverse("incidents"))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, "Suspicious login activity")
