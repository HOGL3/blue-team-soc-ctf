from django.contrib.auth.models import User
from django.db import models


class EmploymentStatus(models.TextChoices):
    ACTIVE = "Active", "Active"
    ON_LEAVE = "On Leave", "On Leave"
    RESIGNED = "Resigned", "Resigned"


class Shift(models.TextChoices):
    MORNING = "Morning", "Morning"
    EVENING = "Evening", "Evening"
    NIGHT = "Night", "Night"


class SecurityClearance(models.TextChoices):
    LOW = "Low", "Low"
    MEDIUM = "Medium", "Medium"
    HIGH = "High", "High"
    CRITICAL = "Critical", "Critical"


class Role(models.TextChoices):
    ADMINISTRATOR = "Administrator", "Administrator"
    SOC_MANAGER = "SOC Manager", "SOC Manager"
    SOC_ANALYST = "SOC Analyst", "SOC Analyst"
    READ_ONLY_ANALYST = "Read Only Analyst", "Read Only Analyst"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    employee_id = models.CharField(
        max_length=50, unique=True, help_text="Unique employee identifier"
    )
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    extension_number = models.CharField(max_length=10, blank=True, null=True)
    office_location = models.CharField(max_length=100)
    shift = models.CharField(
        max_length=20, choices=Shift.choices, default=Shift.MORNING
    )
    employment_status = models.CharField(
        max_length=20, choices=EmploymentStatus.choices, default=EmploymentStatus.ACTIVE
    )
    security_clearance = models.CharField(
        max_length=20, choices=SecurityClearance.choices, default=SecurityClearance.LOW
    )
    role = models.CharField(
        max_length=50, choices=Role.choices, default=Role.SOC_ANALYST
    )
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    is_on_duty = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.employee_id}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]


class DeveloperNote(models.Model):
    title = models.CharField(max_length=200)
    note = models.TextField(help_text="Internal notes for developers only.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Developer Note"
        verbose_name_plural = "Developer Notes"
        ordering = ["-created_at"]
