from django.contrib.auth.models import User
from django.db import models


class AssetCriticality(models.TextChoices):
    LOW = "Low", "Low"
    MEDIUM = "Medium", "Medium"
    HIGH = "High", "High"
    CRITICAL = "Critical", "Critical"


class AssetStatus(models.TextChoices):
    ACTIVE = "Active", "Active"
    OFFLINE = "Offline", "Offline"
    MAINTENANCE = "Maintenance", "Maintenance"
    RETIRED = "Retired", "Retired"


class AssetType(models.TextChoices):
    WORKSTATION = "Workstation", "Workstation"
    SERVER = "Server", "Server"
    FIREWALL = "Firewall", "Firewall"
    ROUTER = "Router", "Router"
    SWITCH = "Switch", "Switch"
    VIRTUAL_MACHINE = "Virtual Machine", "Virtual Machine"
    CLOUD_INSTANCE = "Cloud Instance", "Cloud Instance"


class Asset(models.Model):
    asset_name = models.CharField(max_length=150, unique=True)
    hostname = models.CharField(max_length=150, blank=True, null=True)
    asset_type = models.CharField(max_length=50, choices=AssetType.choices)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    operating_system = models.CharField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_assets",
    )
    location = models.CharField(max_length=200, blank=True, null=True)
    criticality = models.CharField(
        max_length=20, choices=AssetCriticality.choices, default=AssetCriticality.LOW
    )
    status = models.CharField(
        max_length=20, choices=AssetStatus.choices, default=AssetStatus.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.asset_name} ({self.ip_address})"

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"
        ordering = ["-created_at"]
