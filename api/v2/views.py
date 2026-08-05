from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Notification, Role, UserProfile
from activity_logs.models import ActivityLog
from assets.models import Asset
from incidents.models import Incident
from reports.models import Report

from .permissions import (
    IsAdmin,
    IsAdminOrManager,
    IsAdminOrManagerOrAssignedAnalyst,
    IsOwnerOrAssignedAnalyst,
)
from .serializers import (
    ActivityLogSerializer,
    AssetSerializer,
    IncidentSerializer,
    NotificationSerializer,
    ReportSerializer,
    UserProfileSerializer,
)


class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.select_related("assigned_to", "created_by").all()
    serializer_class = IncidentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdminOrManagerOrAssignedAnalyst,
    ]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "severity", "category"]
    search_fields = ["incident_id", "title", "description"]
    ordering_fields = ["created_at", "updated_at", "severity"]

    def perform_update(self, serializer):
        user = self.request.user
        role = getattr(user.profile, "role", None) if hasattr(user, "profile") else None

        if role == Role.SOC_ANALYST:
            if "assigned_to" in serializer.validated_data:
                serializer.validated_data.pop("assigned_to")

        serializer.save()


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.select_related("owner").all()
    serializer_class = AssetSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "criticality", "asset_type"]
    search_fields = ["asset_name", "hostname", "ip_address"]
    ordering_fields = ["created_at"]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminOrManager()]


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.select_related("incident", "author").all()
    serializer_class = ReportSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["report_status"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminOrManager()]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related("user").all()
    serializer_class = UserProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__username", "employee_id"]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        if self.request.method in ["PUT", "PATCH"]:
            return [permissions.IsAuthenticated(), IsOwnerOrAssignedAnalyst()]
        return [permissions.IsAuthenticated(), IsAdmin()]

    @action(
        detail=False,
        methods=["get", "put", "patch"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        profile = getattr(request.user, "profile", None)
        if not profile:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.method == "GET":
            serializer = self.get_serializer(profile)
            return Response(serializer.data)

        serializer = self.get_serializer(
            profile, data=request.data, partial=(request.method == "PATCH")
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAssignedAnalyst]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["is_read"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        return Notification.objects.select_related("user").filter(
            user=self.request.user
        )

    @action(detail=False, methods=["get"])
    def unread(self, request):
        qs = self.get_queryset().filter(is_read=False)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        notif = self.get_object()
        notif.is_read = True
        notif.save()
        return Response({"status": "Notification marked as read"})

    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({"status": "All notifications marked as read"})


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.select_related("user").all()
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrManager]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["action_type"]
    search_fields = ["performed_by__username", "description"]
    ordering_fields = ["timestamp"]


class DashboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {
            "total_incidents": Incident.objects.count(),
            "open_incidents": Incident.objects.filter(status="Open").count(),
            "critical_incidents": Incident.objects.filter(severity="Critical").count(),
            "closed_incidents": Incident.objects.filter(status="Closed").count(),
            "total_assets": Asset.objects.count(),
            "active_assets": Asset.objects.filter(status="Active").count(),
            "reports_generated": Report.objects.count(),
            "unread_notifications": Notification.objects.filter(
                user=request.user, is_read=False
            ).count(),
        }

        distribution = Incident.objects.values("severity").annotate(
            count=Count("severity")
        )
        data["incident_severity_distribution"] = {
            item["severity"]: item["count"] for item in distribution
        }

        recent_logs = ActivityLog.objects.all().order_by("-timestamp")[:5]
        data["recent_activities"] = ActivityLogSerializer(recent_logs, many=True).data

        return Response(data)


class SearchAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q", "")
        if not query:
            return Response({"results": []})

        incidents = Incident.objects.filter(
            title__icontains=query
        ) | Incident.objects.filter(incident_id__icontains=query)
        assets = Asset.objects.filter(
            asset_name__icontains=query
        ) | Asset.objects.filter(hostname__icontains=query)
        reports = Report.objects.filter(title__icontains=query)
        users = User.objects.filter(username__icontains=query)

        return Response(
            {
                "incidents": IncidentSerializer(incidents[:10], many=True).data,
                "assets": AssetSerializer(assets[:10], many=True).data,
                "reports": ReportSerializer(reports[:10], many=True).data,
                "users": [{"id": u.id, "username": u.username} for u in users[:10]],
            }
        )


class HealthAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        db_status = "ok"
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
        except Exception:
            db_status = "down"

        return Response(
            {
                "status": "healthy" if db_status == "ok" else "degraded",
                "database": db_status,
                "version": "1.0",
                "timestamp": timezone.now().isoformat(),
            }
        )


class PlatformStatusAPIView(APIView):
    """
    Returns current platform status.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            "status": "operational"
        })


class AdminForbiddenAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN
        )


class ProfileSingularAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = getattr(request.user, "profile", None)
        return Response({
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "role": profile.role if profile else "Employee",
            "department": profile.department if profile else "",
            "designation": profile.designation if profile else ""
        })


class NotificationCountAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        recent_notifications = Notification.objects.filter(user=request.user).order_by("-created_at")[:5]
        
        return Response({
            "unread_count": unread_count,
            "recent_notifications": [
                {
                    "id": n.id,
                    "title": n.title,
                    "message": n.message,
                    "created_at": n.created_at.isoformat(),
                    "is_read": n.is_read
                } for n in recent_notifications
            ]
        })
