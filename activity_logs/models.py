from django.contrib.auth.models import User
from django.db import models


class ActivityType(models.TextChoices):
    LOGIN = "Login", "Login"
    LOGOUT = "Logout", "Logout"
    CREATE = "Create", "Create"
    UPDATE = "Update", "Update"
    DELETE = "Delete", "Delete"
    ASSIGN = "Assign", "Assign"
    UPLOAD = "Upload", "Upload"


class ActivityLog(models.Model):
    performed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="activity_logs"
    )
    action_type = models.CharField(max_length=20, choices=ActivityType.choices)
    target_object = models.CharField(
        max_length=200,
        help_text="The object that was acted upon (e.g., Incident-1234, Report-56)",
    )
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.performed_by.username} - {self.action_type} - {self.timestamp}"

    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
        ordering = ["-timestamp"]
