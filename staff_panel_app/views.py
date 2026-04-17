from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from accounts_app.models import ChatUser
from messages_app.models import Message, Reaction
from notifications_app.models import Notification
from notifications_app.services import create_broadcast_notifications
from profiles_app.models import Profile
from rooms_app.models import Category, Membership, Room

from .forms import BroadcastNotificationForm


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class StaffDashboardView(StaffRequiredMixin, TemplateView):
    template_name = "staff_panel_app/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "user_count": ChatUser.objects.count(),
                "profile_count": Profile.objects.count(),
                "room_count": Room.objects.count(),
                "category_count": Category.objects.count(),
                "membership_count": Membership.objects.count(),
                "message_count": Message.objects.count(),
                "reaction_count": Reaction.objects.count(),
                "notification_count": Notification.objects.count(),
                "unread_notification_count": Notification.objects.filter(is_read=False).count(),
                "recent_users": ChatUser.objects.order_by("-date_joined")[:5],
                "recent_rooms": Room.objects.select_related("creator", "category").order_by("-id")[:5],
                "recent_messages": Message.objects.select_related("sender", "room").order_by("-created_at")[:5],
                "recent_notifications": Notification.objects.select_related("recipient", "actor", "room").order_by("-created_at")[:5],
                "broadcast_form": kwargs.get("broadcast_form", BroadcastNotificationForm()),
            }
        )
        return context


class StaffBroadcastView(StaffRequiredMixin, View):
    def post(self, request):
        form = BroadcastNotificationForm(request.POST)
        if form.is_valid():
            create_broadcast_notifications(
                room=form.cleaned_data["room"],
                actor=request.user.profile,
                text=form.cleaned_data["text"],
            )
            return redirect("staff_dashboard")
        return StaffDashboardView.as_view()(request, broadcast_form=form)
