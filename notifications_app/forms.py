from django import forms

from .models import Notification


class NotificationFilterForm(forms.Form):
    notification_type = forms.ChoiceField(
        choices=[("", "All types"), *Notification.TYPE_CHOICES],
        required=False,
        label="Notification Type",
    )
    unread_only = forms.BooleanField(required=False, label="Unread only")

