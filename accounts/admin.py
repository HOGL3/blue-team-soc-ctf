from django.contrib import admin

from .models import DeveloperNote, Notification, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "employee_id",
        "department",
        "designation",
        "shift",
        "employment_status",
        "is_on_duty",
    )
    search_fields = ("user__username", "employee_id", "department", "designation")
    list_filter = ("shift", "employment_status", "security_clearance", "is_on_duty")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("user__username",)
    list_per_page = 50
    fieldsets = (
        ("User Information", {"fields": ("user", "employee_id", "profile_image")}),
        (
            "Job Details",
            {
                "fields": (
                    "department",
                    "designation",
                    "shift",
                    "employment_status",
                    "is_on_duty",
                )
            },
        ),
        (
            "Contact & Location",
            {"fields": ("phone_number", "extension_number", "office_location")},
        ),
        ("Security", {"fields": ("security_clearance",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "is_read", "created_at")
    search_fields = ("user__username", "title")
    list_filter = ("is_read", "created_at")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    list_per_page = 50
    fieldsets = (
        ("Notification", {"fields": ("user", "title", "message", "is_read")}),
        ("Timestamps", {"fields": ("created_at",)}),
    )


@admin.register(DeveloperNote)
class DeveloperNoteAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "note")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    list_per_page = 50
    fieldsets = (
        ("Note Details", {"fields": ("title", "note")}),
        ("Timestamps", {"fields": ("created_at",)}),
    )
