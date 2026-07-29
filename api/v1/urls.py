from django.urls import path

from .views import (
    LegacyAdminView,
    LegacyAssetView,
    LegacyAuditLogView,
    LegacyBackupView,
    LegacyConfigView,
    LegacyDashboardView,
    LegacyHealthView,
    LegacyIncidentView,
    LegacyMigrationView,
    LegacyReportView,
    LegacyServicesView,
    LegacySystemView,
    LegacyUsersView,
)

urlpatterns = [
    path("dashboard/", LegacyDashboardView.as_view(), name="legacy-dashboard"),
    path("incidents/", LegacyIncidentView.as_view(), name="legacy-incidents"),
    path(
        "incidents/<int:pk>/",
        LegacyIncidentView.as_view(),
        name="legacy-incident-detail",
    ),
    path("assets/", LegacyAssetView.as_view(), name="legacy-assets"),
    path("assets/<int:pk>/", LegacyAssetView.as_view(), name="legacy-asset-detail"),
    path("reports/", LegacyReportView.as_view(), name="legacy-reports"),
    path("reports/<int:pk>/", LegacyReportView.as_view(), name="legacy-report-detail"),
    path("admin/", LegacyAdminView.as_view(), name="legacy-admin"),
    path("system/", LegacySystemView.as_view(), name="legacy-system"),
    path("health/", LegacyHealthView.as_view(), name="legacy-health"),
    path("config/", LegacyConfigView.as_view(), name="legacy-config"),
    path("backups/", LegacyBackupView.as_view(), name="legacy-backups"),
    path("backups/<int:pk>/", LegacyBackupView.as_view(), name="legacy-backup-detail"),
    path("users/", LegacyUsersView.as_view(), name="legacy-users"),
    path("users/<int:pk>/", LegacyUsersView.as_view(), name="legacy-user-detail"),
    path("audit/", LegacyAuditLogView.as_view(), name="legacy-audit"),
    path("audit/<int:pk>/", LegacyAuditLogView.as_view(), name="legacy-audit-detail"),
    path("migration/", LegacyMigrationView.as_view(), name="legacy-migration"),
    path("services/", LegacyServicesView.as_view(), name="legacy-services"),
]
