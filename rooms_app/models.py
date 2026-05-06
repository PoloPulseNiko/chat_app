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
    VISIBILITY_PUBLIC = "public"
    VISIBILITY_PRIVATE = "private"
    VISIBILITY_STAFF = "staff"

    VISIBILITY_CHOICES = [
        (VISIBILITY_PUBLIC, "Public"),
        (VISIBILITY_PRIVATE, "Private (members only)"),
        (VISIBILITY_STAFF, "Staff Only"),
    ]

    POSTING_MEMBERS = "members"
    POSTING_MODERATORS = "moderators"
    POSTING_STAFF = "staff"

    POSTING_CHOICES = [
        (POSTING_MEMBERS, "Any room member"),
        (POSTING_MODERATORS, "Room moderators only"),
        (POSTING_STAFF, "Staff only"),
    ]

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
    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default=VISIBILITY_PUBLIC,
    )
    posting_policy = models.CharField(
        max_length=20,
        choices=POSTING_CHOICES,
        default=POSTING_MEMBERS,
    )

    def __str__(self):
        return self.name

    def is_member(self, profile):
        if not profile:
            return False
        return self.members.filter(pk=profile.pk).exists()

    def is_moderator(self, profile):
        if not profile:
            return False
        if self.creator_id == profile.pk:
            return True
        return self.memberships.filter(profile=profile, role=Membership.MODERATOR).exists()

    def can_view(self, user=None, profile=None):
        if user and user.is_staff:
            return True
        if self.visibility == self.VISIBILITY_PUBLIC:
            return True
        if self.visibility == self.VISIBILITY_PRIVATE:
            return self.is_member(profile)
        return False

    def can_join(self, user=None, profile=None):
        if not profile or (user and user.is_staff):
            return False
        if self.visibility != self.VISIBILITY_PUBLIC:
            return False
        return not self.is_member(profile)

    def can_post(self, user=None, profile=None):
        if not self.can_view(user=user, profile=profile):
            return False
        if user and user.is_staff:
            return True
        if self.posting_policy == self.POSTING_MEMBERS:
            return self.is_member(profile)
        if self.posting_policy == self.POSTING_MODERATORS:
            return self.is_moderator(profile)
        return False


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
