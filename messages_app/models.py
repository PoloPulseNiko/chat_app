from django.db import models


class Message(models.Model):
    sender = models.ForeignKey("profiles_app.Profile", on_delete=models.CASCADE, related_name="messages")
    room = models.ForeignKey("rooms_app.Room", on_delete=models.CASCADE, related_name="messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} in {self.room}"


class Reaction(models.Model):
    LIKE = "like"
    LOVE = "love"
    LAUGH = "laugh"

    REACTION_CHOICES = [
        (LIKE, "Like"),
        (LOVE, "Love"),
        (LAUGH, "Laugh"),
    ]

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="reactions",
    )
    profile = models.ForeignKey(
        "profiles_app.Profile",
        on_delete=models.CASCADE,
        related_name="reactions",
    )
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("message", "profile", "reaction_type")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.profile} reacted to message {self.message_id}"
