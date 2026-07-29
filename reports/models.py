from django.contrib.auth.models import User
from django.db import models

from incidents.models import Incident


class ReportStatus(models.TextChoices):
    DRAFT = "Draft", "Draft"
    SUBMITTED = "Submitted", "Submitted"
    APPROVED = "Approved", "Approved"


class ReportType(models.TextChoices):
    INCIDENT_REPORT = "Incident Report", "Incident Report"
    DAILY_REPORT = "Daily Report", "Daily Report"
    WEEKLY_REPORT = "Weekly Report", "Weekly Report"
    MONTHLY_REPORT = "Monthly Report", "Monthly Report"


class Report(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    report_type = models.CharField(max_length=50, choices=ReportType.choices)
    report_status = models.CharField(
        max_length=20, choices=ReportStatus.choices, default=ReportStatus.DRAFT
    )
    incident = models.ForeignKey(
        Incident,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports",
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="authored_reports"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.report_type})"

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        ordering = ["-created_at"]
