from django import forms

from .models import Asset


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            "asset_name",
            "hostname",
            "asset_type",
            "ip_address",
            "mac_address",
            "operating_system",
            "owner",
            "location",
            "criticality",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_config = {
            "asset_name": {
                "autocomplete": "off",
                "placeholder": "Enter asset name…",
            },
            "hostname": {
                "autocomplete": "off",
                "placeholder": "server-01…",
                "spellcheck": "false",
            },
            "ip_address": {
                "autocomplete": "off",
                "placeholder": "192.168.1.10…",
                "inputmode": "decimal",
                "spellcheck": "false",
            },
            "mac_address": {
                "autocomplete": "off",
                "placeholder": "00:11:22:33:44:55…",
                "spellcheck": "false",
            },
            "operating_system": {
                "autocomplete": "off",
                "placeholder": "Windows Server 2022…",
            },
            "location": {
                "autocomplete": "street-address",
                "placeholder": "Enter office or rack location…",
            },
        }
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = (
                "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            )
            if field_name in field_config:
                field.widget.attrs.update(field_config[field_name])

        self.fields["owner"].empty_label = "Unassigned"

