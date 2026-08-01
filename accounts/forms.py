import os

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import UserProfile


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_config = {
            "first_name": {
                "autocomplete": "given-name",
                "placeholder": "Enter first name…",
            },
            "last_name": {
                "autocomplete": "family-name",
                "placeholder": "Enter last name…",
            },
            "email": {
                "autocomplete": "email",
                "placeholder": "name@example.com…",
                "spellcheck": "false",
            },
        }
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control", **field_config[name]})


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "phone_number",
            "extension_number",
            "office_location",
            "profile_image",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_config = {
            "phone_number": {
                "autocomplete": "tel",
                "placeholder": "+1 555 010 2020…",
                "inputmode": "tel",
            },
            "extension_number": {
                "autocomplete": "off",
                "placeholder": "Enter extension…",
                "inputmode": "numeric",
            },
            "office_location": {
                "autocomplete": "organization-title",
                "placeholder": "Enter office location…",
            },
        }
        for field_name, field in self.fields.items():
            if field_name != "profile_image":
                field.widget.attrs.update({"class": "form-control", **field_config[field_name]})
            else:
                field.widget.attrs.update(
                    {
                        "class": "form-control",
                        "accept": "image/*",
                        "aria-describedby": "profile-image-help",
                    }
                )

    def clean_profile_image(self):
        image = self.cleaned_data.get("profile_image")
        if image:
            if image.size > 2 * 1024 * 1024:
                raise ValidationError("Image file too large ( > 2MB )")
            ext = os.path.splitext(image.name)[1].lower()
            valid_extensions = [".jpg", ".jpeg", ".png"]
            if ext not in valid_extensions:
                raise ValidationError(
                    "Unsupported file extension. Allowed: jpg, jpeg, png."
                )
        return image

