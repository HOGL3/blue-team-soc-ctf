from django.urls import path

from . import views

urlpatterns = [
    path("", views.IncidentListView.as_view(), name="incidents"),
    path("create/", views.IncidentCreateView.as_view(), name="incident_create"),
    path(
        "<str:incident_id>/", views.IncidentDetailView.as_view(), name="incident_detail"
    ),
    path(
        "<str:incident_id>/edit/",
        views.IncidentUpdateView.as_view(),
        name="incident_update",
    ),
    path(
        "<str:incident_id>/delete/",
        views.IncidentDeleteView.as_view(),
        name="incident_delete",
    ),
]
