from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    nickname = models.CharField(max_length=30, unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)

    def clean(self):
        if len(self.nickname) < 3:
            raise ValidationError("Nickname must be at least 3 characters.")

    def __str__(self):
        return self.nickname
