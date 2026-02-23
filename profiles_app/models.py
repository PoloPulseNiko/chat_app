from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class Profile(models.Model):
    nickname = models.CharField(max_length=30, unique=True)
    bio = models.TextField(blank=True)

    def clean(self):
        if len(self.nickname) < 3:
            raise ValidationError("Nickname must be at least 3 characters.")