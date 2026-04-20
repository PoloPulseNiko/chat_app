from .services import ensure_user_profile

def current_profile(request):
    if not request.user.is_authenticated:
        return {"current_profile": None}
    return {"current_profile": ensure_user_profile(request.user)}
