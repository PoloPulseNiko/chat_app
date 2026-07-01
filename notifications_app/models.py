from django.urls import reverse
from django.db import models


class Notification(models.Model):
    MESSAGE = "message"
    ROOM = "room"
    INVITE = "invite"
    DIRECT_MESSAGE = "direct_message"

    TYPE_CHOICES = [
        (MESSAGE, "Message"),
        (ROOM, "Room"),
        (INVITE, "Invite"),
        (DIRECT_MESSAGE, "Direct message"),
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
    direct_message = models.ForeignKey(
        "messages_app.DirectMessage",
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

    @property
    def target_url(self):
        if self.direct_message_id:
            return reverse(
                "direct_conversation_detail",
                kwargs={"pk": self.direct_message.conversation_id},
            ) + f"#direct-message-{self.direct_message_id}"
        if self.message_id and self.room_id:
            return reverse("room_detail", kwargs={"pk": self.room_id}) + f"#message-{self.message_id}"
        if self.room_id:
            return reverse("room_detail", kwargs={"pk": self.room_id})
        return reverse("notification_list")
