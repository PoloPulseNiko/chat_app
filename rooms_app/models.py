from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey("profiles_app.Profile", on_delete=models.CASCADE)
    members = models.ManyToManyField("profiles_app.Profile", related_name="rooms")

