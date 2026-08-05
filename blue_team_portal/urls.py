from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

from dashboard.views import help_view, release_notes_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt",
        content_type="text/plain",
    ), name="robots_txt"),
    path("", RedirectView.as_view(url="/dashboard/", permanent=False)),
    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("incidents/", include("incidents.urls")),
    path("reports/", include("reports.urls")),
    path("assets/", include("assets.urls")),
    path("activity/", include("activity_logs.urls")),
    path("api/", include("api.urls")),
    path("release-notes/", release_notes_view, name="release_notes_root"),
    path("help/", help_view, name="help_root"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

