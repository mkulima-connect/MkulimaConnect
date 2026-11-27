from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "role")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "username",
            "email",
            "bio",
            "crops_grown",
            "favorite_crops",
            "farm_size",
            "location",
            "phone_number",
            "profile_picture",
        ]
