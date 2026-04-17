from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from accounts_app.services import ensure_user_profile
from messages_app.forms import MessageForm
from notifications_app.services import create_message_notifications, create_room_notifications

from .api_views import RoomDetailAPIView, RoomListAPIView, RoomMessagesAPIView
from .forms import RoomFilterForm, RoomForm
from .models import Membership, Room


class RoomOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        room = self.get_object()
        profile = ensure_user_profile(self.request.user)
        return bool(profile and room.creator == profile)


class RoomListView(ListView):
    model = Room
    template_name = "rooms_app/room_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        queryset = Room.objects.select_related("creator", "category").prefetch_related("members", "tags")
        self.filter_form = RoomFilterForm(self.request.GET or None)
        if self.filter_form.is_valid():
            search = self.filter_form.cleaned_data.get("search")
            category = self.filter_form.cleaned_data.get("category")
            tag = self.filter_form.cleaned_data.get("tag")
            sort = self.filter_form.cleaned_data.get("sort") or "name"
            if search:
                queryset = queryset.filter(name__icontains=search)
            if category:
                queryset = queryset.filter(category=category)
            if tag:
                queryset = queryset.filter(tags=tag)
            queryset = queryset.order_by(sort).distinct()
        return queryset

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
        is_member = bool(user_profile and room.members.filter(pk=user_profile.pk).exists())

        context["messages"] = room.messages.select_related("sender").prefetch_related("reactions__profile")
        context["form"] = kwargs.get("form", MessageForm())
        context["is_member"] = is_member
        context["can_manage_room"] = bool(user_profile and room.creator_id == user_profile.pk)
        context["can_post_message"] = is_member
        context["reaction_choices"] = [
            ("like", "Like"),
            ("love", "Love"),
            ("laugh", "Laugh"),
        ]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect("login")
        profile = ensure_user_profile(request.user)
        if not profile or not self.object.members.filter(pk=profile.pk).exists():
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

    def form_valid(self, form):
        room = form.save(commit=False)
        room.creator = ensure_user_profile(self.request.user)
        room.save()
        form.save_m2m()
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
        profile = ensure_user_profile(request.user)

        room.members.add(profile)
        Membership.objects.get_or_create(profile=profile, room=room)
        return redirect("room_detail", pk=room.pk)


class RoomLeaveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        profile = ensure_user_profile(request.user)

        if room.creator_id != profile.pk:
            room.members.remove(profile)
            Membership.objects.filter(profile=profile, room=room).delete()
        return redirect("room_detail", pk=room.pk)
