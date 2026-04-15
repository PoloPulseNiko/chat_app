from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from messages_app.forms import MessageForm
from notifications_app.services import create_message_notifications, create_room_notifications
from profiles_app.models import Profile

from .forms import RoomForm
from .models import Membership, Room


class RoomOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        room = self.get_object()
        return self.request.user.is_authenticated and room.creator == self.request.user.profile


class RoomListView(ListView):
    model = Room
    template_name = "rooms_app/room_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        return Room.objects.select_related("creator", "category").prefetch_related("members")


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
        user_profile = getattr(self.request.user, "profile", None)
        is_member = bool(user_profile and room.members.filter(pk=user_profile.pk).exists())

        context["messages"] = room.messages.select_related("sender").prefetch_related("reactions__profile")
        context["form"] = kwargs.get("form", MessageForm())
        context["is_member"] = is_member
        context["can_manage_room"] = bool(user_profile and room.creator_id == user_profile.pk)
        context["can_post_message"] = is_member
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect("login")
        if not self.object.members.filter(pk=request.user.profile.pk).exists():
            return redirect("room_detail", pk=self.object.pk)

        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile
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

    def form_valid(self, form):
        room = form.save(commit=False)
        room.creator = self.request.user.profile
        room.save()
        room.members.add(room.creator)
        Membership.objects.get_or_create(profile=room.creator, room=room)
        return redirect("room_list")


class RoomUpdateView(LoginRequiredMixin, RoomOwnerRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = "rooms_app/room_form.html"

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
        profile = request.user.profile

        room.members.add(profile)
        Membership.objects.get_or_create(profile=profile, room=room)
        return redirect("room_detail", pk=room.pk)


class RoomLeaveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        profile = request.user.profile

        if room.creator_id != profile.pk:
            room.members.remove(profile)
            Membership.objects.filter(profile=profile, room=room).delete()
        return redirect("room_detail", pk=room.pk)
