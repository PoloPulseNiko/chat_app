from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from accounts_app.services import ensure_user_profile
from messages_app.models import Message
from notifications_app.models import Notification
from rooms_app.models import Membership, Room

from .forms import ProfileForm
from .models import Profile


class ProfileOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        profile = self.get_object()
        return self.request.user.is_authenticated and profile.user == self.request.user


class ProfileListView(ListView):
    model = Profile
    template_name = "profiles_app/profile_list.html"
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profiles_app/profile_detail.html"
    context_object_name = "profile"


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profiles_app/profile_form.html"

    def dispatch(self, request, *args, **kwargs):
        profile = ensure_user_profile(request.user)
        if profile:
            return redirect("profile_edit", pk=profile.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()
        return redirect("profile_list")


class ProfileUpdateView(LoginRequiredMixin, ProfileOwnerRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profiles_app/profile_form.html"

    def get_success_url(self):
        return reverse_lazy("profile_detail", kwargs={"pk": self.object.pk})


class ProfileDeleteView(LoginRequiredMixin, ProfileOwnerRequiredMixin, DeleteView):
    model = Profile
    template_name = "profiles_app/profile_confirm_delete.html"
    success_url = reverse_lazy("profile_list")

    def form_valid(self, form):
        user = self.object.user
        response = super().form_valid(form)
        user.delete()
        return response


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "profiles_app/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = ensure_user_profile(self.request.user)

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
