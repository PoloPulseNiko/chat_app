from django.contrib.auth import get_user_model

from profiles_app.models import Profile


UserModel = get_user_model()


def build_unique_nickname(base_nickname: str) -> str:
    nickname = base_nickname
    counter = 1

    while Profile.objects.filter(nickname=nickname).exists():
        counter += 1
        nickname = f"{base_nickname}-{counter}"

    return nickname


def ensure_user_profile(user: UserModel | None):
    if not user or not getattr(user, "is_authenticated", False):
        return None

    try:
        return user.profile
    except Profile.DoesNotExist:
        base_nickname = user.display_name or user.username or f"user-{user.pk}"
        return Profile.objects.create(
            user=user,
            nickname=build_unique_nickname(base_nickname),
        )
