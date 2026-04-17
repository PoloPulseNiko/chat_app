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
