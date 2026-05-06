from django import forms
from .models import Category, Room, Tag


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "description", "category", "tags", "visibility", "posting_policy"]
        labels = {
            "name": "Room Name",
            "description": "Description",
            "category": "Category",
            "tags": "Tags",
            "visibility": "Visibility",
            "posting_policy": "Who Can Post",
        }
        help_texts = {
            "name": "Enter a unique room name (3-100 characters)",
            "description": "Describe what this room is about",
            "category": "Pick a topic so users can browse similar rooms",
            "tags": "Assign a few tags to make the room easier to discover",
            "visibility": "Staff can decide whether a room is public, private, or staff-only.",
            "posting_policy": "Staff can control who is allowed to send messages in this room.",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "My Awesome Room", "maxlength": "100"}),
            "description": forms.Textarea(attrs={"placeholder": "What is this room about?", "rows": 4, "maxlength": "500"}),
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["name"].widget.attrs["readonly"] = True
        if not (user and user.is_staff):
            self.fields.pop("visibility")
            self.fields.pop("posting_policy")

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if self.instance and self.instance.pk:
            return self.instance.name
        if len(name) < 3:
            raise forms.ValidationError("Room name must be at least 3 characters long.")
        if len(name) > 100:
            raise forms.ValidationError("Room name cannot exceed 100 characters.")
        return name


class RoomFilterForm(forms.Form):
    search = forms.CharField(required=False, max_length=50, label="Search")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label="All categories")
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), required=False, empty_label="All tags")
    sort = forms.ChoiceField(
        choices=[
            ("name", "Name"),
            ("-id", "Newest"),
        ],
        required=False,
        initial="name",
    )

    def clean_search(self):
        search = self.cleaned_data.get("search", "").strip()
        if search and len(search) < 2:
            raise forms.ValidationError("Search term must be at least 2 characters long.")
        return search
