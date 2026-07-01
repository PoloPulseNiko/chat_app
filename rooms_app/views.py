from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from accounts_app.services import ensure_user_profile
from messages_app.forms import MessageForm
from notifications_app.models import Notification
from notifications_app.services import (
    create_invitation_notifications,
    create_message_notifications,
    create_room_notifications,
)

from .api_views import RoomDetailAPIView, RoomListAPIView, RoomMessagesAPIView
from .forms import RoomFilterForm, RoomForm, RoomInvitationForm
from .models import Membership, Room, RoomInvitation


class RoomOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_staff:
            return True
        room = self.get_object()
        profile = ensure_user_profile(self.request.user)
        return bool(profile and room.creator == profile)


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = "rooms_app/room_list.html"
    context_object_name = "rooms"

    login_url = "/accounts/login/"
    redirect_field_name = "next"

    def get_queryset(self):
        queryset = Room.objects.select_related("creator", "category").prefetch_related("members", "tags")
        profile = ensure_user_profile(self.request.user)
        if self.request.user.is_staff:
            visible_rooms = queryset
        elif profile:
            visible_rooms = queryset.filter(
                Q(visibility=Room.VISIBILITY_PUBLIC) | Q(members=profile)
            )
        else:
            visible_rooms = queryset.filter(visibility=Room.VISIBILITY_PUBLIC)

        self.filter_form = RoomFilterForm(self.request.GET or None)

        if self.filter_form.is_valid():
            search = self.filter_form.cleaned_data.get("search")
            category = self.filter_form.cleaned_data.get("category")
            tag = self.filter_form.cleaned_data.get("tag")
            sort = self.filter_form.cleaned_data.get("sort") or "name"

            if search:
                visible_rooms = visible_rooms.filter(name__icontains=search)
            if category:
                visible_rooms = visible_rooms.filter(category=category)
            if tag:
                visible_rooms = visible_rooms.filter(tags=tag)

            visible_rooms = visible_rooms.order_by(sort).distinct()

        return visible_rooms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.filter_form
        return context


class RoomDetailView(DetailView):
    model = Room
    template_name = "rooms_app/room_detail.html"
    context_object_name = "room"

    def get_queryset(self):
        return Room.objects.select_related("creator", "category").prefetch_related(
            "members",
            "messages__sender",
            "messages__reactions__profile",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.object
        user_profile = ensure_user_profile(self.request.user)
        is_member = room.is_member(user_profile)
        can_view_content = room.can_view_content(user=self.request.user, profile=user_profile)

        context["messages"] = (
            room.messages.select_related("sender").prefetch_related("reactions__profile")
            if can_view_content
            else room.messages.none()
        )
        context["form"] = kwargs.get("form", MessageForm())
        context["is_member"] = is_member
        context["can_manage_room"] = bool(
            self.request.user.is_staff or (user_profile and room.creator_id == user_profile.pk)
        )
        context["can_view_content"] = can_view_content
        context["can_post_message"] = room.can_post(user=self.request.user, profile=user_profile)
        context["can_view_room"] = room.can_view(user=self.request.user, profile=user_profile)
        context["can_join_room"] = room.can_join(user=self.request.user, profile=user_profile)
        context["requires_invite"] = room.join_policy == Room.JOIN_INVITE
        context["invite_form"] = RoomInvitationForm(room=room)
        context["pending_invites"] = room.invitations.select_related("invitee", "invited_by").filter(
            accepted_at__isnull=True
        )[:8]
        context["reaction_choices"] = [
            ("like", "Like"),
            ("love", "Love"),
            ("laugh", "Laugh"),
        ]
        return context

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_profile = ensure_user_profile(request.user)
        if not self.object.can_view(user=request.user, profile=user_profile):
            return redirect("room_list")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect("login")
        profile = ensure_user_profile(request.user)
        if not self.object.can_post(user=request.user, profile=profile):
            return redirect("room_detail", pk=self.object.pk)

        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = profile
            message.room = self.object
            message.save()
            create_message_notifications(message)
            return redirect("room_detail", pk=self.object.pk)

        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = "rooms_app/room_form.html"
    success_url = reverse_lazy("room_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        room = form.save(commit=False)
        room.creator = ensure_user_profile(self.request.user)
        room.save()
        form.save_m2m()
        room.members.add(room.creator)
        Membership.objects.get_or_create(
            profile=room.creator,
            room=room,
            defaults={"role": Membership.MODERATOR},
        )
        return redirect("room_list")


class RoomUpdateView(LoginRequiredMixin, RoomOwnerRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = "rooms_app/room_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        create_room_notifications(self.object)
        return response

    def get_success_url(self):
        return reverse_lazy("room_detail", kwargs={"pk": self.object.pk})


class RoomDeleteView(LoginRequiredMixin, RoomOwnerRequiredMixin, DeleteView):
    model = Room
    template_name = "rooms_app/room_confirm_delete.html"
    success_url = reverse_lazy("room_list")


class RoomJoinView(LoginRequiredMixin, View):
    def post(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        profile = ensure_user_profile(request.user)

        if not room.can_join(user=request.user, profile=profile):
            return redirect("room_detail", pk=room.pk)

        room.members.add(profile)
        Membership.objects.get_or_create(profile=profile, room=room)
        RoomInvitation.objects.filter(room=room, invitee=profile, accepted_at__isnull=True).update(
            accepted_at=timezone.now()
        )
        Notification.objects.filter(
            recipient=profile,
            room=room,
            notification_type=Notification.INVITE,
            is_read=False,
        ).update(is_read=True)
        return redirect("room_detail", pk=room.pk)


class RoomLeaveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        profile = ensure_user_profile(request.user)

        if room.creator_id != profile.pk:
            room.members.remove(profile)
            Membership.objects.filter(profile=profile, room=room).delete()
        return redirect("room_detail", pk=room.pk)


class RoomInviteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        room = get_object_or_404(Room, pk=self.kwargs["pk"])
        profile = ensure_user_profile(self.request.user)
        return bool(self.request.user.is_staff or (profile and room.creator_id == profile.pk))

    def post(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        inviter = ensure_user_profile(request.user)
        form = RoomInvitationForm(request.POST, room=room)

        if form.is_valid():
            invitation, _ = RoomInvitation.objects.update_or_create(
                room=room,
                invitee=form.cleaned_data["invitee"],
                defaults={"invited_by": inviter, "accepted_at": None},
            )
            if room.join_policy != Room.JOIN_INVITE:
                room.join_policy = Room.JOIN_INVITE
                room.save(update_fields=["join_policy"])
            create_invitation_notifications(invitation)

        return redirect("room_detail", pk=room.pk)
