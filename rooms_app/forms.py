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
        help_texts = {
            "name": "Enter a unique room name (3-100 characters)",
            "description": "Describe what this room is about",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "My Awesome Room", "maxlength": "100"}),
            "description": forms.Textarea(attrs={"placeholder": "What is this room about?", "rows": 4, "maxlength": "500"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["name"].widget.attrs["readonly"] = True

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if self.instance and self.instance.pk:
            return self.instance.name
        if len(name) < 3:
            raise forms.ValidationError("Room name must be at least 3 characters long.")
        if len(name) > 100:
            raise forms.ValidationError("Room name cannot exceed 100 characters.")
        return name
