from django.contrib.auth.models import User
from django.db import models


class IncidentSeverity(models.TextChoices):
    LOW = "Low", "Low"
    MEDIUM = "Medium", "Medium"
    HIGH = "High", "High"
    CRITICAL = "Critical", "Critical"


class IncidentStatus(models.TextChoices):
    OPEN = "Open", "Open"
    IN_PROGRESS = "In Progress", "In Progress"
    CLOSED = "Closed", "Closed"


class IncidentCategory(models.TextChoices):
    MALWARE = "Malware", "Malware"
    PHISHING = "Phishing", "Phishing"
    BRUTE_FORCE = "Brute Force", "Brute Force"
    DDOS = "DDoS", "DDoS"
    PRIVILEGE_ESCALATION = "Privilege Escalation", "Privilege Escalation"
    DATA_LEAK = "Data Leak", "Data Leak"
    SUSPICIOUS_LOGIN = "Suspicious Login", "Suspicious Login"


class Incident(models.Model):
    incident_id = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique identifier for the incident",
        db_index=True,
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=IncidentCategory.choices)
    severity = models.CharField(max_length=20, choices=IncidentSeverity.choices)
    status = models.CharField(
        max_length=20, choices=IncidentStatus.choices, default=IncidentStatus.OPEN
    )
    source = models.CharField(max_length=100)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_incidents",
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_incidents"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.incident_id} - {self.title}"

    class Meta:
        verbose_name = "Incident"
        verbose_name_plural = "Incidents"
        ordering = ["-created_at"]


class TimelineEvent(models.Model):
    incident = models.ForeignKey(
        Incident, on_delete=models.CASCADE, related_name="timeline_events"
    )
    event = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event for {self.incident.incident_id} at {self.timestamp}"

    class Meta:
        verbose_name = "Timeline Event"
        verbose_name_plural = "Timeline Events"
        ordering = ["-timestamp"]


class Attachment(models.Model):
    incident = models.ForeignKey(
        Incident, on_delete=models.CASCADE, related_name="attachments"
    )
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="uploaded_attachments"
    )
    file = models.FileField(upload_to="attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.incident.incident_id}"

    class Meta:
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"
        ordering = ["-uploaded_at"]
