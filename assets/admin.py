from django.contrib import admin

from .models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "asset_name",
        "hostname",
        "asset_type",
        "ip_address",
        "owner",
        "criticality",
        "status",
        "created_at",
    )
    search_fields = (
        "asset_name",
        "hostname",
        "ip_address",
        "mac_address",
        "owner__username",
    )
    list_filter = ("asset_type", "criticality", "status", "created_at")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    list_per_page = 50
    fieldsets = (
        (
            "Asset Information",
            {"fields": ("asset_name", "asset_type", "hostname", "operating_system")},
        ),
        ("Network Information", {"fields": ("ip_address", "mac_address", "location")}),
        ("Management", {"fields": ("owner", "criticality", "status")}),
        ("Timestamps", {"fields": ("created_at",)}),
    )
