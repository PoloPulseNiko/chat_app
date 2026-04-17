from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey("profiles_app.Profile", on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="rooms",
        null=True,
        blank=True,
    )
    members = models.ManyToManyField("profiles_app.Profile", related_name="rooms")
    tags = models.ManyToManyField(Tag, related_name="rooms", blank=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    MEMBER = "member"
    MODERATOR = "moderator"

    ROLE_CHOICES = [
        (MEMBER, "Member"),
        (MODERATOR, "Moderator"),
    ]

    profile = models.ForeignKey(
        "profiles_app.Profile",
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("profile", "room")
        ordering = ["-joined_at"]

    def __str__(self):
        return f"{self.profile} in {self.room}"
