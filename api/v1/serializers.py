from django.contrib.auth.models import User
from rest_framework import serializers

from activity_logs.models import ActivityLog
from assets.models import Asset
from incidents.models import Incident
from reports.models import Report


class LegacyIncidentSerializer(serializers.ModelSerializer):
    IncidentID = serializers.CharField(source="incident_id")
    Desc = serializers.CharField(source="description")
    SeverityLevel = serializers.CharField(source="severity")
    CurrentStatus = serializers.CharField(source="status")
    LoggedDate = serializers.DateTimeField(source="created_at")

    class Meta:
        model = Incident
        fields = [
            "IncidentID",
            "title",
            "Desc",
            "SeverityLevel",
            "CurrentStatus",
            "LoggedDate",
        ]


class LegacyAssetSerializer(serializers.ModelSerializer):
    AssetTag = serializers.CharField(source="asset_name")
    Host = serializers.CharField(source="hostname")
    SystemType = serializers.CharField(source="asset_type")
    IP = serializers.CharField(source="ip_address")
    IsActive = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = ["AssetTag", "Host", "SystemType", "IP", "IsActive"]

    def get_IsActive(self, obj):
        return obj.status == "Active"


class LegacyReportSerializer(serializers.ModelSerializer):
    ReportID = serializers.IntegerField(source="id")
    Title = serializers.CharField(source="title")
    ArchiveDate = serializers.DateTimeField(source="created_at")

    class Meta:
        model = Report
        fields = ["ReportID", "Title", "ArchiveDate"]


class LegacyUserSerializer(serializers.ModelSerializer):
    Username = serializers.CharField(source="username")
    Department = serializers.SerializerMethodField()
    Role = serializers.SerializerMethodField()
    AccountStatus = serializers.SerializerMethodField()
    LastLogin = serializers.DateTimeField(source="last_login")
    CreatedDate = serializers.DateTimeField(source="date_joined")

    class Meta:
        model = User
        fields = [
            "id",
            "Username",
            "Department",
            "Role",
            "AccountStatus",
            "LastLogin",
            "CreatedDate",
        ]

    def get_Department(self, obj):
        return (
            getattr(obj.profile, "department", "Unknown")
            if hasattr(obj, "profile")
            else "Unknown"
        )

    def get_Role(self, obj):
        return (
            getattr(obj.profile, "role", "Unknown")
            if hasattr(obj, "profile")
            else "Unknown"
        )

    def get_AccountStatus(self, obj):
        return "Active" if obj.is_active else "Disabled"


class LegacyAuditSerializer(serializers.ModelSerializer):
    EventID = serializers.IntegerField(source="id")
    Action = serializers.CharField(source="action_type")
    User = serializers.CharField(source="performed_by.username")
    Timestamp = serializers.DateTimeField(source="timestamp")
    Details = serializers.CharField(source="description")

    class Meta:
        model = ActivityLog
        fields = ["EventID", "Action", "User", "Timestamp", "Details"]
