from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/api/v2/", permanent=False), name="api-root"),
    path("v1/", include("api.v1.urls")),
    path("v2/", include("api.v2.urls")),
]
