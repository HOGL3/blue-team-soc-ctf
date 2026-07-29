from django.urls import path

from . import views

urlpatterns = [
    path("", views.ReportListView.as_view(), name="reports"),
    path("create/", views.ReportCreateView.as_view(), name="report_create"),
    path("<int:pk>/", views.ReportDetailView.as_view(), name="report_detail"),
    path("<int:pk>/edit/", views.ReportUpdateView.as_view(), name="report_update"),
    path("<int:pk>/delete/", views.ReportDeleteView.as_view(), name="report_delete"),
    # Export endpoints
    path(
        "<int:pk>/export/csv/",
        views.ReportCSVExportView.as_view(),
        name="report_export_csv",
    ),
    path(
        "<int:pk>/export/pdf/",
        views.ReportPDFExportView.as_view(),
        name="report_export_pdf",
    ),
]
