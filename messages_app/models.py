from django.db import models

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey("profiles_app.Profile", on_delete=models.CASCADE, related_name="messages")
    room = models.ForeignKey("rooms_app.Room", on_delete=models.CASCADE, related_name="messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
