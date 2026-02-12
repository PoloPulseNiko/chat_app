from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "description"]
        labels = {
            "name": "Room Name",
            "description": "Description",
        }
        widgets = {
            "description": forms.Textarea(attrs={"placeholder": "What is this room about?"}),
        }