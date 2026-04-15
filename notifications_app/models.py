from django.db import models


class Notification(models.Model):
    MESSAGE = "message"
    ROOM = "room"

    TYPE_CHOICES = [
        (MESSAGE, "Message"),
        (ROOM, "Room"),
    ]

    recipient = models.ForeignKey(
        "profiles_app.Profile",
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    actor = models.ForeignKey(
        "profiles_app.Profile",
        on_delete=models.CASCADE,
        related_name="sent_notifications",
    )
    room = models.ForeignKey(
        "rooms_app.Room",
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    message = models.ForeignKey(
        "messages_app.Message",
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    text = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification for {self.recipient}"

