import random
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import (
    Notification,
    SecurityClearance,
    Shift,
)
from activity_logs.models import ActivityLog, ActivityType
from assets.models import Asset, AssetCriticality, AssetStatus, AssetType
from incidents.models import (
    Incident,
    IncidentCategory,
    IncidentSeverity,
    IncidentStatus,
    TimelineEvent,
)
from reports.models import Report, ReportStatus, ReportType


class Command(BaseCommand):
    help = "Seeds the database with realistic SOC environment data for Apex Global Solutions."

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.WARNING("Clearing existing seed data (excluding superusers)...")
        )

        # Clear existing non-superuser data
        User.objects.filter(is_superuser=False).delete()
        Asset.objects.all().delete()
        Incident.objects.all().delete()
        Report.objects.all().delete()
        ActivityLog.objects.all().delete()
        Notification.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Environment cleared. Beginning data generation for Apex Global Solutions..."
            )
        )

        now = timezone.now()

        # --- 1. SEED USERS & PROFILES ---
        employees = [
            {
                "username": "mchen",
                "first": "Michael",
                "last": "Chen",
                "dept": "SOC",
                "desig": "SOC Manager",
                "shift": Shift.MORNING,
                "clearance": SecurityClearance.CRITICAL,
                "email": "m.chen@apexglobal.local",
            },
            {
                "username": "jsmith",
                "first": "Jane",
                "last": "Smith",
                "dept": "SOC",
                "desig": "Senior Security Analyst",
                "shift": Shift.MORNING,
                "clearance": SecurityClearance.HIGH,
                "email": "j.smith@apexglobal.local",
            },
            {
                "username": "tnguyen",
                "first": "Tony",
                "last": "Nguyen",
                "dept": "SOC",
                "desig": "Junior Security Analyst",
                "shift": Shift.EVENING,
                "clearance": SecurityClearance.MEDIUM,
                "email": "t.nguyen@apexglobal.local",
            },
            {
                "username": "rpatel",
                "first": "Raj",
                "last": "Patel",
                "dept": "IT Infrastructure",
                "desig": "Network Administrator",
                "shift": Shift.MORNING,
                "clearance": SecurityClearance.HIGH,
                "email": "r.patel@apexglobal.local",
            },
            {
                "username": "ajohnson",
                "first": "Alice",
                "last": "Johnson",
                "dept": "IT Infrastructure",
                "desig": "System Administrator",
                "shift": Shift.MORNING,
                "clearance": SecurityClearance.HIGH,
                "email": "a.johnson@apexglobal.local",
            },
            {
                "username": "slee",
                "first": "Sarah",
                "last": "Lee",
                "dept": "HR",
                "desig": "HR Manager",
                "shift": Shift.MORNING,
                "clearance": SecurityClearance.MEDIUM,
                "email": "s.lee@apexglobal.local",
            },
            {
                "username": "bwhite",
                "first": "Bob",
                "last": "White",
                "dept": "Finance",
                "desig": "Finance Officer",
                "shift": Shift.MORNING,
                "clearance": SecurityClearance.HIGH,
                "email": "b.white@apexglobal.local",
            },
        ]

        created_users = {}
        for idx, emp in enumerate(employees):
            user = User.objects.create_user(
                username=emp["username"],
                email=emp["email"],
                password="Password123!",
                first_name=emp["first"],
                last_name=emp["last"],
            )
            created_users[emp["username"]] = user

            profile = user.profile
            profile.employee_id = f"AGS-{1000 + idx}"
            profile.department = emp["dept"]
            profile.designation = emp["desig"]
            profile.phone_number = f"+1-555-01{random.randint(10, 99)}"
            profile.extension_number = f"x{random.randint(100, 999)}"
            profile.office_location = (
                "Headquarters - Floor 3"
                if emp["dept"] in ["SOC", "IT Infrastructure"]
                else "Headquarters - Floor 2"
            )
            profile.shift = emp["shift"]
            profile.security_clearance = emp["clearance"]
            profile.save()

            ActivityLog.objects.create(
                performed_by=user,
                action_type=ActivityType.LOGIN,
                target_object="System",
                description="Initial system provisioning login.",
                timestamp=now - timedelta(days=random.randint(20, 30)),
            )

        self.stdout.write(self.style.SUCCESS(f"Created {len(employees)} Employees."))

        # --- 2. SEED ASSETS ---
        assets_data = [
            {
                "name": "AGS-DC-01",
                "host": "dc01.apexglobal.local",
                "ip": "10.0.1.10",
                "os": "Windows Server 2022",
                "type": AssetType.SERVER,
                "crit": AssetCriticality.CRITICAL,
                "status": AssetStatus.ACTIVE,
                "owner": "ajohnson",
            },
            {
                "name": "AGS-DC-02",
                "host": "dc02.apexglobal.local",
                "ip": "10.0.1.11",
                "os": "Windows Server 2022",
                "type": AssetType.SERVER,
                "crit": AssetCriticality.CRITICAL,
                "status": AssetStatus.ACTIVE,
                "owner": "ajohnson",
            },
            {
                "name": "AGS-FW-CORE",
                "host": "fw-core.apexglobal.local",
                "ip": "10.0.0.1",
                "os": "Palo Alto PAN-OS",
                "type": AssetType.FIREWALL,
                "crit": AssetCriticality.CRITICAL,
                "status": AssetStatus.ACTIVE,
                "owner": "rpatel",
            },
            {
                "name": "AGS-WEB-PROD",
                "host": "www.apexglobal.local",
                "ip": "10.0.50.15",
                "os": "Ubuntu 22.04 LTS",
                "type": AssetType.SERVER,
                "crit": AssetCriticality.HIGH,
                "status": AssetStatus.ACTIVE,
                "owner": "ajohnson",
            },
            {
                "name": "AGS-VPN-GW",
                "host": "vpn.apexglobal.local",
                "ip": "10.0.0.5",
                "os": "Cisco ASA",
                "type": AssetType.ROUTER,
                "crit": AssetCriticality.HIGH,
                "status": AssetStatus.ACTIVE,
                "owner": "rpatel",
            },
            {
                "name": "WKSTN-FIN-01",
                "host": "wkstn-fin01.apexglobal.local",
                "ip": "10.0.100.45",
                "os": "Windows 11",
                "type": AssetType.WORKSTATION,
                "crit": AssetCriticality.MEDIUM,
                "status": AssetStatus.ACTIVE,
                "owner": "bwhite",
            },
            {
                "name": "WKSTN-HR-01",
                "host": "wkstn-hr01.apexglobal.local",
                "ip": "10.0.100.82",
                "os": "Windows 11",
                "type": AssetType.WORKSTATION,
                "crit": AssetCriticality.LOW,
                "status": AssetStatus.OFFLINE,
                "owner": "slee",
            },
            {
                "name": "SOC-SIEM-01",
                "host": "siem.apexglobal.local",
                "ip": "10.0.2.50",
                "os": "Red Hat Enterprise Linux 9",
                "type": AssetType.SERVER,
                "crit": AssetCriticality.CRITICAL,
                "status": AssetStatus.ACTIVE,
                "owner": "mchen",
            },
        ]

        created_assets = {}
        for asset in assets_data:
            a = Asset.objects.create(
                asset_name=asset["name"],
                hostname=asset["host"],
                ip_address=asset["ip"],
                operating_system=asset["os"],
                asset_type=asset["type"],
                criticality=asset["crit"],
                status=asset["status"],
                owner=created_users[asset["owner"]],
            )
            a.created_at = now - timedelta(days=random.randint(15, 30))
            a.save()
            created_assets[asset["name"]] = a

            ActivityLog.objects.create(
                performed_by=created_users[asset["owner"]],
                action_type=ActivityType.CREATE,
                target_object=f"Asset: {a.asset_name}",
                description="Asset onboarded into the inventory system.",
                timestamp=a.created_at,
            )

        self.stdout.write(self.style.SUCCESS(f"Created {len(assets_data)} Assets."))

        # --- 3. SEED INCIDENTS ---
        soc_analysts = [
            created_users["jsmith"],
            created_users["tnguyen"],
            created_users["mchen"],
        ]

        incidents_data = [
            {
                "title": "Multiple Failed VPN Logins",
                "desc": "Detected 50+ failed login attempts targeting the legacy VPN Gateway from an external IP address (198.51.100.44). Potential brute force attack in progress on AGS-VPN-GW. Note: Legacy authentication platform is still handling these requests due to the incomplete infrastructure migration.",
                "cat": IncidentCategory.BRUTE_FORCE,
                "sev": IncidentSeverity.HIGH,
                "status": IncidentStatus.IN_PROGRESS,
                "analyst": "tnguyen",
                "source": "SIEM Alert - Firewall Log",
                "days_ago": 2,
            },
            {
                "title": "Suspicious PowerShell Execution",
                "desc": "Endpoint protection blocked a PowerShell script attempting to execute Mimikatz commands on WKSTN-FIN-01.",
                "cat": IncidentCategory.MALWARE,
                "sev": IncidentSeverity.CRITICAL,
                "status": IncidentStatus.OPEN,
                "analyst": "jsmith",
                "source": "Endpoint Detection and Response",
                "days_ago": 0,
            },
            {
                "title": "Data Exfiltration via DNS",
                "desc": "Abnormal volume of DNS TXT queries originating from AGS-WEB-PROD indicating potential DNS tunneling.",
                "cat": IncidentCategory.DATA_LEAK,
                "sev": IncidentSeverity.HIGH,
                "status": IncidentStatus.CLOSED,
                "analyst": "jsmith",
                "source": "Network IDS",
                "days_ago": 14,
            },
            {
                "title": "Unauthorized Access Attempt on SIEM and Legacy Portal",
                "desc": "An internal user attempted to access SOC-SIEM-01 and the archived Management Portal without sufficient privileges. Request denied by ACL. We still need to shut down the older management components to prevent this.",
                "cat": IncidentCategory.PRIVILEGE_ESCALATION,
                "sev": IncidentSeverity.MEDIUM,
                "status": IncidentStatus.CLOSED,
                "analyst": "mchen",
                "source": "SIEM Audit Log",
                "days_ago": 20,
            },
            {
                "title": "Phishing Email Campaign",
                "desc": "Multiple employees reported receiving an email claiming to be from HR requesting immediate password reset targeting WKSTN-HR-01.",
                "cat": IncidentCategory.PHISHING,
                "sev": IncidentSeverity.MEDIUM,
                "status": IncidentStatus.IN_PROGRESS,
                "analyst": "tnguyen",
                "source": "User Report",
                "days_ago": 5,
            },
            {
                "title": "Platform API Cutover \u2013 Validation Monitoring",
                "desc": "As part of the platform modernization programme, Engineering has completed the migration of internal SOC tooling to the current Platform API (v2). During the validation period, a limited number of compatibility services remain operational to support rollback procedures and legacy integrations if required. The SOC has been requested to monitor for unexpected or unusual access patterns involving older management interfaces until the compatibility window is formally closed. No active security incident has been confirmed at this time. Investigation is precautionary. Related Change Request: CHG-2026-047 – Platform API Modernization.",
                "cat": IncidentCategory.SUSPICIOUS_LOGIN,
                "sev": IncidentSeverity.MEDIUM,
                "status": IncidentStatus.OPEN,
                "analyst": "mchen",
                "source": "Change Management / Platform Engineering",
                "days_ago": 1,
            },
        ]

        created_incidents = {}
        for idx, inc in enumerate(incidents_data):
            inc_id = f"INC-{1000 + idx}"
            incident = Incident.objects.create(
                incident_id=inc_id,
                title=inc["title"],
                description=inc["desc"],
                category=inc["cat"],
                severity=inc["sev"],
                status=inc["status"],
                source=inc["source"],
                assigned_to=created_users[inc["analyst"]],
                created_by=created_users["mchen"],  # Manager created
            )
            incident.created_at = now - timedelta(days=inc["days_ago"])
            if inc["status"] == IncidentStatus.CLOSED:
                incident.resolved_at = incident.created_at + timedelta(days=1)
            incident.save()
            created_incidents[inc["title"]] = incident

            TimelineEvent.objects.create(
                incident=incident,
                event="Initial triage completed by SOC team.",
                timestamp=incident.created_at + timedelta(minutes=30),
            )

            ActivityLog.objects.create(
                performed_by=created_users["mchen"],
                action_type=ActivityType.CREATE,
                target_object=inc_id,
                description=f"Incident '{incident.title}' was recorded.",
                timestamp=incident.created_at,
            )

            Notification.objects.create(
                user=created_users[inc["analyst"]],
                title="New Incident Assigned",
                message=f"You have been assigned to {inc_id}: {incident.title}",
                is_read=True if inc["days_ago"] > 3 else False,
            )

        self.stdout.write(
            self.style.SUCCESS(f"Created {len(incidents_data)} Incidents.")
        )

        # --- 4. SEED REPORTS ---
        reports_data = [
            {
                "title": "Post-Incident RCA: DNS Exfiltration",
                "desc": "Executive summary regarding the DNS tunneling attempt. The root cause was identified as a compromised third-party plugin. The plugin was removed and firewall rules were strictly enforced to drop unauthorized outbound DNS queries.",
                "type": ReportType.INCIDENT_REPORT,
                "status": ReportStatus.APPROVED,
                "inc": "Data Exfiltration via DNS",
                "author": "jsmith",
                "days_ago": 12,
            },
            {
                "title": "Weekly Threat Intelligence Digest",
                "desc": "Overview of emerging threats targeting the financial sector, including active ransomware campaigns and associated Indicators of Compromise (IoCs).",
                "type": ReportType.WEEKLY_REPORT,
                "status": ReportStatus.APPROVED,
                "inc": None,
                "author": "mchen",
                "days_ago": 7,
            },
            {
                "title": "Draft RCA: Unauthorized Access",
                "desc": "Draft investigation notes regarding the attempted access to the SIEM and the Legacy Portal. Waiting on confirmation from network team regarding when the temporary compatibility mode for the legacy system will be permanently disabled.",
                "type": ReportType.INCIDENT_REPORT,
                "status": ReportStatus.DRAFT,
                "inc": "Unauthorized Access Attempt on SIEM and Legacy Portal",
                "author": "mchen",
                "days_ago": 19,
            },
        ]

        for rep in reports_data:
            report = Report.objects.create(
                title=rep["title"],
                description=rep["desc"],
                report_type=rep["type"],
                report_status=rep["status"],
                incident=created_incidents[rep["inc"]] if rep["inc"] else None,
                author=created_users[rep["author"]],
            )
            report.created_at = now - timedelta(days=rep["days_ago"])
            report.save()

            ActivityLog.objects.create(
                performed_by=created_users[rep["author"]],
                action_type=ActivityType.CREATE,
                target_object=f"Report-{report.pk}",
                description=f"Authored report: {report.title}",
                timestamp=report.created_at,
            )

            if rep["status"] == ReportStatus.APPROVED:
                Notification.objects.create(
                    user=created_users["mchen"],
                    title="Report Approved",
                    message=f"The report '{report.title}' has been finalized and approved.",
                    is_read=True,
                )

        self.stdout.write(self.style.SUCCESS(f"Created {len(reports_data)} Reports."))

        # Inject explicit migration audit logs
        ActivityLog.objects.create(
            performed_by=created_users["mchen"],
            action_type=ActivityType.UPDATE,
            target_object="System Migration",
            description="Migration completed except for one legacy service. Older management components remain online for compatibility.",
            timestamp=now - timedelta(days=25),
        )

        ActivityLog.objects.create(
            performed_by=created_users["ajohnson"],
            action_type=ActivityType.UPDATE,
            target_object="Legacy Services",
            description="Legacy services restarted. Archive server synchronized.",
            timestamp=now - timedelta(days=15),
        )

        self.stdout.write(
            self.style.WARNING("=============================================")
        )
        self.stdout.write(
            self.style.SUCCESS("Apex Global Solutions environment seeded successfully!")
        )
        self.stdout.write(
            self.style.SUCCESS(
                "Login with any employee username (e.g., mchen) and password 'Password123!'"
            )
        )
        self.stdout.write(
            self.style.WARNING("=============================================")
        )
