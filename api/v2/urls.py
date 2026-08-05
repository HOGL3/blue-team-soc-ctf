from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from .views import (
    ActivityLogViewSet,
    AssetViewSet,
    DashboardAPIView,
    HealthAPIView,
    IncidentViewSet,
    NotificationViewSet,
    PlatformStatusAPIView,
    ReportViewSet,
    SearchAPIView,
    UserProfileViewSet,
    AdminForbiddenAPIView,
    ProfileSingularAPIView,
    NotificationCountAPIView,
)

router = DefaultRouter()
router.register(r"incidents", IncidentViewSet, basename="incident")
router.register(r"assets", AssetViewSet, basename="asset")
router.register(r"reports", ReportViewSet, basename="report")
router.register(r"profiles", UserProfileViewSet, basename="profile")
router.register(r"notifications", NotificationViewSet, basename="notification")
router.register(r"activity-logs", ActivityLogViewSet, basename="activitylog")

urlpatterns = [
    path("profile/", ProfileSingularAPIView.as_view(), name="profile-api-singular"),
    path("notifications/", NotificationCountAPIView.as_view(), name="notifications-count-api"),
    path("admin/", AdminForbiddenAPIView.as_view(), name="admin-forbidden-api"),
    path("", include(router.urls)),
    path("dashboard/", DashboardAPIView.as_view(), name="dashboard-api"),
    path("search/", SearchAPIView.as_view(), name="search-api"),
    path("health/", HealthAPIView.as_view(), name="health-api"),
    path("status/", PlatformStatusAPIView.as_view(), name="status-api"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

