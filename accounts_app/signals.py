from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from .services import build_unique_nickname


UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        from profiles_app.models import Profile

        base_nickname = instance.display_name or instance.username
        Profile.objects.create(user=instance, nickname=build_unique_nickname(base_nickname))


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name != "accounts_app":
        return

    moderator_group, _ = Group.objects.get_or_create(name="Moderators")
    room_manager_group, _ = Group.objects.get_or_create(name="Room Managers")

    moderator_permissions = Permission.objects.filter(
        codename__in=["view_profile", "change_profile", "delete_profile"]
    )
    room_manager_permissions = Permission.objects.filter(
        codename__in=["view_room", "add_room", "change_room", "delete_room"]
    )

    moderator_group.permissions.set(moderator_permissions)
    room_manager_group.permissions.set(room_manager_permissions)
