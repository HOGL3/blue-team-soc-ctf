from django import forms
from django.contrib.auth.models import User

from .models import Incident


class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            "incident_id",
            "title",
            "description",
            "category",
            "severity",
            "status",
            "source",
            "assigned_to",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_config = {
            "incident_id": {
                "autocomplete": "off",
                "placeholder": "Enter incident ID…",
                "spellcheck": "false",
            },
            "title": {
                "autocomplete": "off",
                "placeholder": "Summarize the incident…",
            },
            "description": {
                "autocomplete": "off",
                "placeholder": "Describe what happened, impact, and scope…",
                "rows": 5,
            },
            "source": {
                "autocomplete": "off",
                "placeholder": "Email alert, SIEM, analyst review…",
            },
        }
        for name, field in self.fields.items():
            field.widget.attrs["class"] = (
                "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            )
            if name in field_config:
                field.widget.attrs.update(field_config[name])

        self.fields["assigned_to"].empty_label = "Unassigned"
        self.fields["assigned_to"].queryset = User.objects.filter(
            is_active=True
        ).order_by("username")


class IncidentUpdateForm(IncidentForm):
    pass

