from .services import ensure_user_profile


def current_profile(request):
    return {"current_profile": ensure_user_profile(request.user)}
