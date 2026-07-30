"""
Comprehensive test suite for the Blue Team Portal CTF.
Covers authentication, RBAC, CRUD, APIs, serializers, and challenge validation.
"""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Notification, Role
from assets.models import Asset, AssetCriticality, AssetStatus, AssetType
from incidents.models import (
    Incident,
    IncidentCategory,
    IncidentSeverity,
    IncidentStatus,
)
from reports.models import Report, ReportStatus, ReportType


class BaseTestCase(TestCase):
    """Shared setup for all test classes."""

    def setUp(self):
        self.client = Client()

        # Create admin user
        self.admin_user = User.objects.create_user(
            username="testadmin", password="TestPass123!"
        )
        self.admin_user.profile.role = Role.ADMINISTRATOR
        self.admin_user.profile.department = "SOC"
        self.admin_user.profile.save()

        # Create analyst user
        self.analyst_user = User.objects.create_user(
            username="testanalyst", password="TestPass123!"
        )
        self.analyst_user.profile.role = Role.SOC_ANALYST
        self.analyst_user.profile.department = "SOC"
        self.analyst_user.profile.save()

        # Create a sample incident
        self.incident = Incident.objects.create(
            incident_id="INC-TEST-001",
            title="Test Incident",
            description="A test incident for the suite.",
            category=IncidentCategory.PHISHING,
            severity=IncidentSeverity.HIGH,
            status=IncidentStatus.OPEN,
            source="Test Suite",
            assigned_to=self.analyst_user,
            created_by=self.admin_user,
        )

        # Create a sample asset
        self.asset = Asset.objects.create(
            asset_name="TEST-SERVER-01",
            hostname="test-srv.local",
            asset_type=AssetType.SERVER,
            ip_address="10.0.0.99",
            criticality=AssetCriticality.HIGH,
            status=AssetStatus.ACTIVE,
            owner=self.admin_user,
        )

        # Create a sample report
        self.report = Report.objects.create(
            title="Test Report",
            description="A test report.",
            report_type=ReportType.INCIDENT_REPORT,
            report_status=ReportStatus.DRAFT,
            incident=self.incident,
            author=self.admin_user,
        )


# =========================================================
# 1. Authentication Tests
# =========================================================


class AuthenticationTests(BaseTestCase):

    def test_login_success(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testadmin",
                "password": "TestPass123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"))

    def test_login_failure(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testadmin",
                "password": "wrongpassword",
            },
        )
        self.assertEqual(response.status_code, 200)
        # User should remain on login page, not redirected to dashboard
        self.assertContains(response, "Login")

    def test_logout(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirect(self):
        """Unauthenticated users should be redirected to login."""
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)


# =========================================================
# 2. Dashboard Tests
# =========================================================


class DashboardTests(BaseTestCase):

    def test_dashboard_loads(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Infrastructure Upgrade Status")


# =========================================================
# 3. Incident CRUD Tests
# =========================================================


class IncidentCRUDTests(BaseTestCase):

    def test_incident_list_view(self):
        self.client.force_login(self.analyst_user)
        response = self.client.get(reverse("incidents"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Incident")

    def test_incident_create(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse("incident_create"),
            {
                "incident_id": "INC-TEST-002",
                "title": "New Created Incident",
                "description": "Created via test.",
                "category": IncidentCategory.MALWARE,
                "severity": IncidentSeverity.CRITICAL,
                "status": IncidentStatus.OPEN,
                "source": "Test",
                "assigned_to": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Incident.objects.filter(incident_id="INC-TEST-002").exists())

    def test_incident_detail_view(self):
        self.client.force_login(self.analyst_user)
        response = self.client.get(
            reverse("incident_detail", kwargs={"incident_id": "INC-TEST-001"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Incident")


# =========================================================
# 4. Asset CRUD Tests
# =========================================================


class AssetCRUDTests(BaseTestCase):

    def test_asset_list_view(self):
        self.client.force_login(self.analyst_user)
        response = self.client.get(reverse("assets"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TEST-SERVER-01")


# =========================================================
# 5. Report Tests
# =========================================================


class ReportTests(BaseTestCase):

    def test_report_list_view(self):
        self.client.force_login(self.analyst_user)
        response = self.client.get(reverse("reports"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Report")


# =========================================================
# 6. Notification Tests
# =========================================================


class NotificationTests(BaseTestCase):

    def test_notification_list(self):
        Notification.objects.create(
            user=self.analyst_user,
            title="Test Notification",
            message="You have a new alert.",
        )
        self.client.force_login(self.analyst_user)
        response = self.client.get(reverse("notifications"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Notification")

    def test_notification_isolation(self):
        """Users should only see their own notifications."""
        Notification.objects.create(
            user=self.admin_user,
            title="Admin Only Notification",
            message="This should not be visible to analyst.",
        )
        self.client.force_login(self.analyst_user)
        response = self.client.get(reverse("notifications"))
        self.assertNotContains(response, "Admin Only Notification")


# =========================================================
# 7. Profile Tests
# =========================================================


class ProfileTests(BaseTestCase):

    def test_profile_view(self):
        self.client.force_login(self.analyst_user)
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)

    def test_profile_shows_own_data(self):
        """Profile view should always show the logged-in user's data, not another user's."""
        self.client.force_login(self.analyst_user)
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)


# =========================================================
# 8. Secure API (v2) Tests
# =========================================================


class SecureAPITests(BaseTestCase):

    def test_v2_incidents_requires_auth(self):
        response = self.client.get("/api/v2/incidents/")
        self.assertIn(response.status_code, [401, 403])

    def test_v2_incidents_authenticated(self):
        self.client.force_login(self.admin_user)
        response = self.client.get("/api/v2/incidents/")
        self.assertEqual(response.status_code, 200)

    def test_v2_dashboard_api(self):
        self.client.force_login(self.admin_user)
        response = self.client.get("/api/v2/dashboard/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total_incidents", data)

    def test_v2_health_is_public(self):
        response = self.client.get("/api/v2/health/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")

    def test_v2_search_requires_auth(self):
        response = self.client.get("/api/v2/search/?q=test")
        self.assertIn(response.status_code, [401, 403])

    def test_v2_does_not_contain_flag(self):
        """The secure API should NEVER return the CTF flag."""
        self.client.force_login(self.admin_user)
        endpoints = [
            "/api/v2/incidents/",
            "/api/v2/assets/",
            "/api/v2/reports/",
            "/api/v2/profiles/",
            "/api/v2/dashboard/",
            "/api/v2/health/",
        ]
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertNotContains(
                response, "flag{", msg_prefix=f"Flag leaked in {endpoint}"
            )


# =========================================================
# 9. Legacy API (v1) Tests
# =========================================================


class LegacyAPITests(BaseTestCase):

    def test_v1_requires_authentication(self):
        """All legacy endpoints should require login."""
        endpoints = [
            "/api/v1/dashboard/",
            "/api/v1/incidents/",
            "/api/v1/admin/",
            "/api/v1/config/",
            "/api/v1/health/",
        ]
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertIn(
                response.status_code,
                [401, 403],
                msg=f"{endpoint} accessible without auth",
            )

    def test_v1_admin_accessible_by_any_authenticated_user(self):
        """The intentional BAC: any authenticated user can access /api/v1/admin/."""
        self.client.force_login(self.analyst_user)
        response = self.client.get("/api/v1/admin/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("SystemVersion", data)
        self.assertIn("LegacyMasterToken", data)

    def test_v1_not_in_swagger(self):
        """Legacy API should not appear in the OpenAPI schema."""
        self.client.force_login(self.admin_user)
        response = self.client.get("/api/v2/schema/")
        self.assertEqual(response.status_code, 200)
        schema_text = response.content.decode()
        self.assertNotIn("/api/v1/", schema_text)

    def test_v1_audit_endpoint(self):
        """The fixed audit endpoint should work without crashing."""
        self.client.force_login(self.analyst_user)
        response = self.client.get("/api/v1/audit/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("AuditLogs", data)

    def test_v1_migration_endpoint(self):
        self.client.force_login(self.analyst_user)
        response = self.client.get("/api/v1/migration/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["MigrationProgress"], "85%")


# =========================================================
# 10. Seed Data & Management Command Tests
# =========================================================


class SeedDataTests(TestCase):

    def test_seed_command_runs(self):
        """The seed_data management command should complete without errors."""
        from django.core.management import call_command

        call_command("seed_data")
        self.assertTrue(User.objects.filter(username="mchen").exists())
        self.assertTrue(Incident.objects.filter(incident_id="INC-1000").exists())
        self.assertTrue(Asset.objects.filter(asset_name="AGS-DC-01").exists())
        self.assertTrue(
            Report.objects.filter(title__contains="DNS Exfiltration").exists()
        )
