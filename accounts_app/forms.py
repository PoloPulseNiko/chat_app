from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import ChatUser


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ChatUser
        fields = ("username", "email", "display_name", "password1", "password2")
        labels = {
            "display_name": "Display Name",
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Choose a username"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "display_name": forms.TextInput(attrs={"placeholder": "What should people call you?"}),
        }

