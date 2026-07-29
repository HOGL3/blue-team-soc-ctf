from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from accounts.models import Notification, UserProfile
from activity_logs.models import ActivityLog
from assets.models import Asset
from incidents.models import Incident
from reports.models import Report


@login_required
def dashboard_view(request):
    """
    Main SOC Dashboard view.
    """

    # ==========================
    # Summary Counts
    # ==========================
    total_incidents = Incident.objects.count()
    open_incidents = Incident.objects.filter(status="Open").count()
    closed_incidents = Incident.objects.filter(status="Closed").count()

    total_assets = Asset.objects.count()
    active_assets = Asset.objects.filter(status="Active").count()

    total_reports = Report.objects.count()
    draft_reports = Report.objects.filter(report_status="Draft").count()

    active_notifications = Notification.objects.filter(
        user=request.user, is_read=False
    ).count()

    total_notifications = Notification.objects.filter(user=request.user).count()

    # ==========================
    # Recent Records
    # ==========================
    recent_incidents = Incident.objects.select_related("assigned_to").order_by(
        "-created_at"
    )[:5]

    recent_assets = Asset.objects.select_related("owner").order_by("-created_at")[:5]

    recent_reports = Report.objects.select_related("author").order_by("-created_at")[:5]

    recent_activity = ActivityLog.objects.select_related("performed_by").order_by(
        "-timestamp"
    )[:5]

    recent_notifications_list = Notification.objects.filter(
        user=request.user, is_read=False
    ).order_by("-created_at")[:5]

    # ==========================
    # User Profile
    # ==========================
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    # ==========================
    # Incident Analytics
    # ==========================
    incidents_by_severity = list(
        Incident.objects.values("severity")
        .annotate(count=Count("severity"))
        .order_by("-count")
    )

    incidents_by_status = list(
        Incident.objects.values("status")
        .annotate(count=Count("status"))
        .order_by("-count")
    )

    incidents_by_category = list(
        Incident.objects.values("category")
        .annotate(count=Count("category"))
        .order_by("-count")
    )

    # ==========================
    # Asset Analytics
    # ==========================
    assets_by_type = list(
        Asset.objects.values("asset_type")
        .annotate(count=Count("asset_type"))
        .order_by("-count")
    )

    assets_by_criticality = list(
        Asset.objects.values("criticality")
        .annotate(count=Count("criticality"))
        .order_by("-count")
    )

    assets_by_status = list(
        Asset.objects.values("status")
        .annotate(count=Count("status"))
        .order_by("-count")
    )

    # ==========================
    # Report Analytics
    # ==========================
    reports_by_type = list(
        Report.objects.values("report_type")
        .annotate(count=Count("report_type"))
        .order_by("-count")
    )

    reports_by_status = list(
        Report.objects.values("report_status")
        .annotate(count=Count("report_status"))
        .order_by("-count")
    )

    now = timezone.now()

    reports_this_month = Report.objects.filter(
        created_at__year=now.year, created_at__month=now.month
    ).count()

    # ==========================
    # Activity Analytics
    # ==========================
    recent_activity_count = ActivityLog.objects.filter(
        timestamp__gte=now - timedelta(days=7)
    ).count()

    most_common_activity_qs = (
        ActivityLog.objects.values("action_type")
        .annotate(count=Count("action_type"))
        .order_by("-count")
        .first()
    )

    most_common_activity_name = (
        most_common_activity_qs["action_type"]
        if most_common_activity_qs
        else "No Activity"
    )

    # ==========================
    # Template Context
    # ==========================
    context = {
        "total_incidents": total_incidents,
        "open_incidents": open_incidents,
        "closed_incidents": closed_incidents,
        "total_assets": total_assets,
        "active_assets": active_assets,
        "total_reports": total_reports,
        "draft_reports": draft_reports,
        "active_notifications": active_notifications,
        "total_notifications": total_notifications,
        "recent_incidents": recent_incidents,
        "recent_assets": recent_assets,
        "recent_reports": recent_reports,
        "recent_activity": recent_activity,
        "recent_notifications_list": recent_notifications_list,
        "user_profile": user_profile,
        "incidents_by_severity": incidents_by_severity,
        "incidents_by_status": incidents_by_status,
        "incidents_by_category": incidents_by_category,
        "assets_by_type": assets_by_type,
        "assets_by_criticality": assets_by_criticality,
        "assets_by_status": assets_by_status,
        "reports_by_type": reports_by_type,
        "reports_by_status": reports_by_status,
        "reports_this_month": reports_this_month,
        "recent_activity_count": recent_activity_count,
        "most_common_activity_name": most_common_activity_name,
    }

    return render(request, "dashboard.html", context)
