from django import forms

from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            "title",
            "description",
            "report_type",
            "report_status",
            "incident",
            "author",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_config = {
            "title": {
                "autocomplete": "off",
                "placeholder": "Name this report…",
            },
            "description": {
                "autocomplete": "off",
                "placeholder": "Summarize findings, evidence, and next steps…",
                "rows": 6,
            },
        }
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = (
                "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            )
            if field_name in field_config:
                field.widget.attrs.update(field_config[field_name])

        self.fields["incident"].empty_label = "No Linked Incident"
        self.fields["author"].widget = forms.HiddenInput()

