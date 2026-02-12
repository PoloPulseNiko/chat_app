from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["nickname", "bio"]
        labels = {
            "nickname": "Your Nickname",
            "bio": "Short Bio",
        }
        help_texts = {
            "nickname": "Choose a unique nickname",
            "bio": "Tell us a little about yourself (optional)",
        }
        widgets = {
            "bio": forms.Textarea(attrs={"placeholder": "I love tech..."}),
        }
