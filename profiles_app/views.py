from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from messages_app.models import Message
from notifications_app.models import Notification
from rooms_app.models import Membership, Room

from .models import Profile
from .forms import ProfileForm

def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, "profiles_app/profile_list.html", {"profiles": profiles})

def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, "profiles_app/profile_detail.html", {"profile": profile})

@login_required
def profile_create(request):
    if hasattr(request.user, "profile"):
        return redirect("profile_edit", pk=request.user.profile.pk)

    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("profile_list")
    else:
        form = ProfileForm()
    return render(request, "profiles_app/profile_form.html", {"form": form})

@login_required
def profile_edit(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if profile.user != request.user:
        return redirect("profile_detail", pk=profile.pk)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile_detail", pk=profile.pk)
    else:
        form = ProfileForm(instance=profile)
    return render(request, "profiles_app/profile_form.html", {"form": form})

@login_required
def profile_delete(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if profile.user != request.user:
        return redirect("profile_detail", pk=profile.pk)

    if request.method == "POST":
        user = profile.user
        profile.delete()
        user.delete()
        return redirect("profile_list")
    return render(request, "profiles_app/profile_confirm_delete.html", {"profile": profile})


class DashboardView(TemplateView):
    template_name = "profiles_app/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile

        created_rooms = Room.objects.filter(creator=profile).select_related("category")
        memberships = Membership.objects.filter(profile=profile).select_related("room", "room__category")
        joined_rooms = [membership.room for membership in memberships if membership.room.creator_id != profile.pk]
        recent_messages = Message.objects.filter(sender=profile).select_related("room").order_by("-created_at")[:5]
        notifications = Notification.objects.filter(recipient=profile).select_related("actor", "room").order_by("-created_at")[:5]

        context.update(
            {
                "profile": profile,
                "created_rooms": created_rooms,
                "joined_rooms": joined_rooms,
                "recent_messages": recent_messages,
                "notifications": notifications,
                "unread_notifications_count": Notification.objects.filter(recipient=profile, is_read=False).count(),
            }
        )
        return context
