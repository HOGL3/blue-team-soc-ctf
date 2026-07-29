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
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


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
        for field_name, field in self.fields.items():
            if field_name != "profile_image":
                field.widget.attrs.update({"class": "form-control"})
            else:
                field.widget.attrs.update(
                    {"class": "form-control", "accept": "image/*"}
                )

    def clean_profile_image(self):
        image = self.cleaned_data.get("profile_image")
        if image:
            # Check file size (e.g., limit to 2MB)
            if image.size > 2 * 1024 * 1024:
                raise ValidationError("Image file too large ( > 2MB )")
            # Check file extension
            ext = os.path.splitext(image.name)[1].lower()
            valid_extensions = [".jpg", ".jpeg", ".png"]
            if ext not in valid_extensions:
                raise ValidationError(
                    "Unsupported file extension. Allowed: jpg, jpeg, png."
                )
        return image
