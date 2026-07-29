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
        # Apply Bootstrap styling to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = (
                "form-select"
                if isinstance(field.widget, forms.Select)
                else "form-control"
            )

        self.fields["incident"].empty_label = "No Linked Incident"
        self.fields["description"].widget.attrs["rows"] = 5

        # Hide author field visually in the UI, as it will be populated by the view automatically
        # Alternatively, we can make it readonly or disabled. For now, we keep it hidden.
        self.fields["author"].widget = forms.HiddenInput()
