from django.db import models

# Create your models here.
class Profile(models.Model):
    nickname = models.CharField(max_length=30, unique=True)
    bio = models.TextField(blank=True)