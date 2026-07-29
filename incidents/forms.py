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
        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "form-select"
                if isinstance(field.widget, forms.Select)
                else "form-control"
            )

        self.fields["assigned_to"].empty_label = "Unassigned"
        self.fields["assigned_to"].queryset = User.objects.filter(
            is_active=True
        ).order_by("username")


class IncidentUpdateForm(IncidentForm):
    pass
