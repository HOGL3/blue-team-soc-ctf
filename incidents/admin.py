from django.contrib import admin

from .models import Attachment, Incident, TimelineEvent


class TimelineEventInline(admin.TabularInline):
    model = TimelineEvent
    extra = 1
    readonly_fields = ("timestamp",)


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1
    readonly_fields = ("uploaded_at",)


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = (
        "incident_id",
        "title",
        "category",
        "severity",
        "status",
        "assigned_to",
        "created_at",
    )
    search_fields = ("incident_id", "title", "description", "source")
    list_filter = ("status", "severity", "category", "created_at")
    readonly_fields = ("created_at", "updated_at")
    inlines = [TimelineEventInline, AttachmentInline]
    ordering = ("-created_at",)
    list_per_page = 50
    fieldsets = (
        ("Incident Information", {"fields": ("incident_id", "title", "description")}),
        ("Classification", {"fields": ("category", "severity", "status", "source")}),
        ("Assignment", {"fields": ("assigned_to", "created_by")}),
        ("Timestamps", {"fields": ("created_at", "updated_at", "resolved_at")}),
    )


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ("incident", "event", "timestamp")
    search_fields = ("incident__incident_id", "event")
    list_filter = ("timestamp",)
    readonly_fields = ("timestamp",)
    ordering = ("-timestamp",)
    list_per_page = 50


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("incident", "uploaded_by", "file", "uploaded_at")
    search_fields = ("incident__incident_id", "uploaded_by__username", "file")
    list_filter = ("uploaded_at",)
    readonly_fields = ("uploaded_at",)
    ordering = ("-uploaded_at",)
    list_per_page = 50
