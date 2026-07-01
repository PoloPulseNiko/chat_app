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

    JOIN_OPEN = "open"
    JOIN_INVITE = "invite"

    JOIN_CHOICES = [
        (JOIN_OPEN, "Anyone can join"),
        (JOIN_INVITE, "Invite required"),
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
    join_policy = models.CharField(
        max_length=20,
        choices=JOIN_CHOICES,
        default=JOIN_OPEN,
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

    def has_pending_invite(self, profile):
        if not profile:
            return False
        return self.invitations.filter(invitee=profile, accepted_at__isnull=True).exists()

    def can_view(self, user=None, profile=None):
        if user and user.is_staff:
            return True
        if self.visibility == self.VISIBILITY_PUBLIC:
            return True
        if self.visibility == self.VISIBILITY_PRIVATE:
            return self.is_member(profile) or self.has_pending_invite(profile)
        return False

    def can_view_content(self, user=None, profile=None):
        if user and user.is_staff:
            return True
        return self.is_member(profile)

    def can_join(self, user=None, profile=None):
        if not profile or (user and user.is_staff):
            return False
        if not self.can_view(user=user, profile=profile):
            return False
        if self.join_policy == self.JOIN_INVITE:
            return self.has_pending_invite(profile)
        return not self.is_member(profile)

    def can_post(self, user=None, profile=None):
        if not self.can_view_content(user=user, profile=profile):
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


class RoomInvitation(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="invitations",
    )
    invitee = models.ForeignKey(
        "profiles_app.Profile",
        on_delete=models.CASCADE,
        related_name="room_invitations",
    )
    invited_by = models.ForeignKey(
        "profiles_app.Profile",
        on_delete=models.SET_NULL,
        related_name="sent_room_invitations",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("room", "invitee")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.invitee} invited to {self.room}"
