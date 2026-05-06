from django import forms

from rooms_app.models import Room


class BroadcastNotificationForm(forms.Form):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), label="Target Room")
    text = forms.CharField(
        max_length=255,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Write a short staff announcement"}),
        help_text="This message will be sent to room members as a notification.",
    )

    def clean_text(self):
        text = self.cleaned_data["text"].strip()
        if len(text) < 10:
            raise forms.ValidationError("Broadcast message must be at least 10 characters long.")
        return text


class RoomAccessControlForm(forms.Form):
    room = forms.ModelChoiceField(
        queryset=Room.objects.select_related("creator", "category").order_by("name"),
        label="Target Room",
    )
    visibility = forms.ChoiceField(
        choices=Room.VISIBILITY_CHOICES,
        label="Visibility",
        help_text="Control who can see this room.",
    )
    posting_policy = forms.ChoiceField(
        choices=Room.POSTING_CHOICES,
        label="Who Can Post",
        help_text="Control who can send messages in this room.",
    )

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get("room")
        if room:
            if "visibility" not in cleaned_data or not cleaned_data["visibility"]:
                cleaned_data["visibility"] = room.visibility
            if "posting_policy" not in cleaned_data or not cleaned_data["posting_policy"]:
                cleaned_data["posting_policy"] = room.posting_policy
        return cleaned_data
