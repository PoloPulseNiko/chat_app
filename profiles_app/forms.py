from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["nickname", "bio", "avatar"]
        labels = {
            "nickname": "Your Nickname",
            "bio": "Short Bio",
            "avatar": "Profile Picture",
        }
        help_texts = {
            "nickname": "Choose a unique nickname (3-30 characters)",
            "bio": "Tell us a little about yourself (optional, max 500 characters)",
            "avatar": "Upload a profile picture to personalize your account.",
        }
        widgets = {
            "nickname": forms.TextInput(attrs={"placeholder": "Enter your nickname", "maxlength": "30"}),
            "bio": forms.Textarea(attrs={"placeholder": "I love tech...", "rows": 4, "maxlength": "500"}),
            "avatar": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and not (user and user.is_staff):
            self.fields["nickname"].widget.attrs["readonly"] = True

    def clean_nickname(self):
        nickname = self.cleaned_data.get("nickname")
        if self.instance and self.instance.pk:
            return self.instance.nickname
        if len(nickname) < 3:
            raise forms.ValidationError("Nickname must be at least 3 characters long.")
        return nickname
