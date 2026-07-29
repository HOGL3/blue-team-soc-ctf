from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "report_type",
        "report_status",
        "author",
        "incident",
        "created_at",
    )
    search_fields = (
        "title",
        "description",
        "author__username",
        "incident__incident_id",
    )
    list_filter = ("report_type", "report_status", "created_at")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    list_per_page = 50
    fieldsets = (
        (
            "Report Details",
            {"fields": ("title", "description", "report_type", "report_status")},
        ),
        ("Relationships", {"fields": ("author", "incident")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
