from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from activity_logs.models import ActivityLog
from assets.models import Asset
from incidents.models import Incident
from reports.models import Report

from .serializers import (
    LegacyAssetSerializer,
    LegacyAuditSerializer,
    LegacyIncidentSerializer,
    LegacyReportSerializer,
    LegacyUserSerializer,
)


class LegacyAdminPermission(permissions.BasePermission):
    """
    VULNERABILITY: Broken Access Control
    Legacy LDAP integration was stripped during the v1 -> v2 migration.
    This permission was temporarily hardcoded to True to prevent breaking
    older compatibility systems, but it was never updated to use the new RBAC.
    """

    def has_permission(self, request, view):
        # TODO: Restore proper role checks once v2 LDAP is fully integrated.
        return True


class LegacyDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(exclude=True)
    def get(self, request):
        return Response(
            {
                "ActiveAlerts": Incident.objects.filter(status="Open").count(),
                "LegacyServersOnline": 4,
                "BackupStatus": "WARNING - 14 Days Overdue",
                "ConnectedSystems": 23,
                "LastMaintenanceDate": "2021-08-14T02:00:00Z",
            }
        )


class LegacyIncidentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(exclude=True)
    def get(self, request, pk=None):
        if pk:
            try:
                incident = Incident.objects.get(pk=pk)
                return Response(LegacyIncidentSerializer(incident).data)
            except Incident.DoesNotExist:
                return Response({"Error": "Record not found"}, status=404)
        incidents = Incident.objects.all()[:20]
        return Response(
            {"Records": LegacyIncidentSerializer(incidents, many=True).data}
        )


class LegacyAssetView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(exclude=True)
    def get(self, request, pk=None):
        hardcoded_assets = [
            {
                "AssetTag": "LEGACY-VPN-01",
                "Host": "vpn-old.apexglobal.local",
                "SystemType": "VPN Gateway",
                "IP": "10.0.0.5",
                "IsActive": True,
            },
            {
                "AssetTag": "BKP-MGT-01",
                "Host": "backup-master",
                "SystemType": "Backup Management Server",
                "IP": "10.0.0.10",
                "IsActive": False,
            },
            {
                "AssetTag": "AUTH-LEGACY",
                "Host": "auth-v1",
                "SystemType": "Old Authentication Server",
                "IP": "10.0.0.15",
                "IsActive": True,
            },
            {
                "AssetTag": "ARCHIVE-FS",
                "Host": "fs-archive",
                "SystemType": "Archive File Server",
                "IP": "10.0.0.20",
                "IsActive": True,
            },
            {
                "AssetTag": "SOC-PORTAL-V1",
                "Host": "soc-legacy",
                "SystemType": "Legacy SOC Portal",
                "IP": "10.0.0.25",
                "IsActive": True,
            },
        ]

        if pk:
            try:
                asset = Asset.objects.get(pk=pk)
                return Response(LegacyAssetSerializer(asset).data)
            except Asset.DoesNotExist:
                return Response({"Error": "Asset not found"}, status=404)

        db_assets = Asset.objects.all()[:5]
        combined = hardcoded_assets + LegacyAssetSerializer(db_assets, many=True).data
        return Response({"Assets": combined})


class LegacyReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(exclude=True)
    def get(self, request, pk=None):
        hardcoded_reports = [
            {
                "ReportID": 9001,
                "Title": "Migration project: Phase 1 signoff",
                "ArchiveDate": "2021-06-01T10:00:00Z",
            },
            {
                "ReportID": 9002,
                "Title": "Temporary compatibility mode enablement",
                "ArchiveDate": "2021-06-15T14:30:00Z",
            },
            {
                "ReportID": 9003,
                "Title": "Old authentication system deprecation plan",
                "ArchiveDate": "2021-07-20T09:15:00Z",
            },
            {
                "ReportID": 9004,
                "Title": "Archived infrastructure audit log",
                "ArchiveDate": "2021-08-05T16:45:00Z",
            },
        ]

        if pk:
            try:
                report = Report.objects.get(pk=pk)
                return Response(LegacyReportSerializer(report).data)
            except Report.DoesNotExist:
                return Response({"Error": "Report not found"}, status=404)

        db_reports = Report.objects.all()[:5]
        combined = (
            hardcoded_reports + LegacyReportSerializer(db_reports, many=True).data
        )
        return Response({"ArchivedReports": combined})


class LegacyAdminView(APIView):
    # Enforces login (Authentication), but fails to enforce roles (Authorization)
    permission_classes = [permissions.IsAuthenticated, LegacyAdminPermission]

    @extend_schema(exclude=True)
    def get(self, request):
        return Response(
            {
                "SystemVersion": "1.0.4-legacy",
                "MigrationStatus": "Incomplete - 85%",
                "BackupConfiguration": "Nightly - Tapes",
                "MaintenanceWindow": "Sunday 02:00-04:00 UTC",
                "InternalNotes": "Do not shut down AUTH-LEGACY until v2 is fully integrated.",
                "LegacyAdministrator": "admin_legacy (inactive)",
                "LegacySystemConfiguration": "/etc/legacy/master.conf",
                "AdministratorContact": "admin@apexglobal.local",
                "InternalMaintenanceSchedule": "Weekly on Sundays",
                "BackupRotationPolicy": "30 days retention, offsite weekly",
                "LegacySoftwareVersions": {
                    "apache": "2.2.14",
                    "mysql": "5.1.73",
                    "php": "5.3.3",
                },
                "MigrationCompletionStatus": "Pending - Network dependencies",
                "DeprecatedServices": ["v1_auth", "legacy_ftp"],
                "LegacyMasterToken": "CTF{m1gr4t10n_d3bt_3xp0s3d}",
            }
        )


class LegacyConfigView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(exclude=True)
    def get(self, request):
        return Response(
            {
                "LegacyApplicationSettings": {"debug": True, "timeout": 3600},
                "BackupSchedule": "02:00 AM Daily",
                "LoggingConfiguration": {"level": "DEBUG", "path": "/var/log/legacy/"},
                "SessionTimeout": 3600,
                "LegacyAuthenticationMode": "Basic",
                "APIVersion": "v1.0.4",
                "CompatibilityMode": "Enabled",
            }
        )


class LegacyBackupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(exclude=True)
    def get(self, request, pk=None):
        backups = [
            {
                "id": 1,
                "BackupName": "Full-System-Legacy",
                "BackupType": "Full",
                "CompletionTime": "2021-08-10T03:00:00Z",
                "BackupStatus": "Success",
                "StorageLocation": "Tape-Drive-A",
                "RetentionPolicy": "7 Years",
            },
            {
                "id": 2,
                "BackupName": "DB-Dump-Legacy",
                "BackupType": "Incremental",
                "CompletionTime": "2021-08-11T03:00:00Z",
                "BackupStatus": "Success",
                "StorageLocation": "NAS-Archive",
                "RetentionPolicy": "30 Days",
            },
            {
                "id": 3,
                "BackupName": "Config-Backup-Legacy",
                "BackupType": "Config",
                "CompletionTime": "2021-08-12T03:00:00Z",
                "BackupStatus": "Failed",
                "StorageLocation": "NAS-Archive",
                "RetentionPolicy": "30 Days",
            },
        ]
        if pk:
            for b in backups:
                if str(b["id"]) == str(pk):
                    return Response(b)
            return Response({"Error": "Backup not found"}, status=404)
        return Response({"Backups": backups})


class LegacyUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(exclude=True)
    def get(self, request, pk=None):
        if pk:
            try:
                user = User.objects.select_related("profile").get(pk=pk)
                return Response(LegacyUserSerializer(user).data)
            except User.DoesNotExist:
                return Response({"Error": "User not found"}, status=404)
        users = User.objects.select_related("profile").all()[:50]
        return Response({"Users": LegacyUserSerializer(users, many=True).data})


class LegacyAuditLogView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(exclude=True)
    def get(self, request, pk=None):
        hardcoded_audits = [
            {
                "EventID": 10001,
                "Action": "Migration Started",
                "User": "admin_legacy",
                "Timestamp": "2021-06-01T10:00:00Z",
                "Details": "Phase 1 migration initiated",
            },
            {
                "EventID": 10002,
                "Action": "Configuration Change",
                "User": "admin_legacy",
                "Timestamp": "2021-06-15T14:30:00Z",
                "Details": "Enabled compatibility mode for v2 APIs",
            },
            {
                "EventID": 10003,
                "Action": "Backup Execution",
                "User": "system",
                "Timestamp": "2021-08-12T03:00:00Z",
                "Details": "Config-Backup-Legacy Failed due to network timeout",
            },
        ]
        if pk:
            try:
                audit = ActivityLog.objects.select_related("performed_by").get(pk=pk)
                return Response(LegacyAuditSerializer(audit).data)
            except ActivityLog.DoesNotExist:
                for a in hardcoded_audits:
                    if str(a["EventID"]) == str(pk):
                        return Response(a)
                return Response({"Error": "Log not found"}, status=404)

        db_audits = ActivityLog.objects.select_related("performed_by").all()[:20]
        combined = hardcoded_audits + LegacyAuditSerializer(db_audits, many=True).data
        return Response({"AuditLogs": combined})


class LegacyMigrationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(exclude=True)
    def get(self, request):
        return Response(
            {
                "MigrationProgress": "85%",
                "ComponentsMigrated": [
                    "Core DB",
                    "User Profiles",
                    "Modern UI",
                    "Alert Engine",
                ],
                "ComponentsPending": ["Legacy Auth", "VPN Gateway", "Archive Storage"],
                "LegacySystemsRetained": ["AUTH-LEGACY", "ARCHIVE-FS"],
                "MigrationCompletionDate": "TBD - Blocked by dependency on AUTH-LEGACY",
                "InternalMigrationNotes": "We cannot fully decommission v1 until the legacy VPN appliance is replaced. Keep API v1 running in stealth mode.",
            }
        )


class LegacyServicesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(exclude=True)
    def get(self, request):
        return Response(
            {
                "Services": [
                    {
                        "ServiceName": "Legacy Authentication Service",
                        "CurrentStatus": "Running",
                        "Version": "1.0.4",
                        "LastRestart": "2021-08-01T00:00:00Z",
                        "Health": "Warning",
                    },
                    {
                        "ServiceName": "Backup Scheduler",
                        "CurrentStatus": "Failing",
                        "Version": "2.1.0",
                        "LastRestart": "2021-08-10T00:00:00Z",
                        "Health": "Critical",
                    },
                    {
                        "ServiceName": "Archive Manager",
                        "CurrentStatus": "Running",
                        "Version": "1.5.2",
                        "LastRestart": "2021-07-15T00:00:00Z",
                        "Health": "OK",
                    },
                    {
                        "ServiceName": "VPN Gateway",
                        "CurrentStatus": "Running",
                        "Version": "4.0.1",
                        "LastRestart": "2021-06-01T00:00:00Z",
                        "Health": "OK",
                    },
                    {
                        "ServiceName": "Reporting Engine",
                        "CurrentStatus": "Stopped",
                        "Version": "1.0.0",
                        "LastRestart": "2021-05-01T00:00:00Z",
                        "Health": "Offline",
                    },
                    {
                        "ServiceName": "Compatibility Layer",
                        "CurrentStatus": "Running",
                        "Version": "1.0.0",
                        "LastRestart": "2021-08-14T02:00:00Z",
                        "Health": "OK",
                    },
                ]
            }
        )


class LegacySystemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(exclude=True)
    def get(self, request):
        return Response(
            {
                "CompatibilityMode": True,
                "EnabledLegacyServices": ["v1_auth", "v1_reports_sync", "v1_vpn"],
                "MigrationCompletionStatus": "Pending final review",
                "ConnectedLegacyModules": 3,
                "LastSynchronizationTime": "2021-08-14T02:00:00Z",
            }
        )


class LegacyHealthView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(exclude=True)
    def get(self, request):
        return Response(
            {
                "LegacyAPIStatus": "Degraded",
                "DatabaseConnection": "OK - ReadOnly",
                "Version": "1.0.4",
                "LastMigrationDate": "2021-08-14T02:00:00Z",
                "OverallServiceStatus": "Maintenance Mode",
            }
        )
