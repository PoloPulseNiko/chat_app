from django.contrib.auth.models import AbstractUser
from django.db import models


class ChatUser(AbstractUser):
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.display_name or self.username

