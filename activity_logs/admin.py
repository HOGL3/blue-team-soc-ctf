from django.contrib import admin

from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("performed_by", "action_type", "target_object", "timestamp")
    search_fields = ("performed_by__username", "target_object", "description")
    list_filter = ("action_type", "timestamp")
    readonly_fields = ("timestamp",)
    ordering = ("-timestamp",)
    list_per_page = 50
    fieldsets = (
        (
            "Activity Detail",
            {"fields": ("performed_by", "action_type", "target_object", "description")},
        ),
        ("Timestamp", {"fields": ("timestamp",)}),
    )
