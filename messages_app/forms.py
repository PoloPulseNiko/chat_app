from django import forms
from .models import DirectMessage, Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={"placeholder": "Type your message...", "rows": 2, "class": "nt-send-on-enter"}
            ),
        }


class DirectMessageForm(forms.ModelForm):
    class Meta:
        model = DirectMessage
        fields = ["text"]
        labels = {"text": "Message"}
        widgets = {
            "text": forms.Textarea(
                attrs={"placeholder": "Type a private message...", "rows": 2, "class": "nt-send-on-enter"}
            ),
        }

    def clean_text(self):
        text = self.cleaned_data["text"].strip()
        if not text:
            raise forms.ValidationError("Message cannot be empty.")
        return text
