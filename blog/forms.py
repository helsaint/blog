from django import forms
from .models import UserResponseModel


class CustomForm(forms.ModelForm):

    class Meta:
        model = UserResponseModel
        fields = ["name", "email", "subject", "message"]
