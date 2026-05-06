from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from accounts_app.services import ensure_user_profile
from messages_app.models import Message

from .models import Room
from .serializers import MessageSerializer, RoomSerializer


class RoomListAPIView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Room.objects.select_related("creator", "category").prefetch_related("tags", "members")
        profile = ensure_user_profile(self.request.user)

        if self.request.user.is_staff:
            return queryset
        if profile:
            return queryset.filter(Q(visibility=Room.VISIBILITY_PUBLIC) | Q(members=profile)).distinct()
        return queryset.filter(visibility=Room.VISIBILITY_PUBLIC)


class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.select_related("creator", "category").prefetch_related("tags", "members")
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        room = super().get_object()
        profile = ensure_user_profile(self.request.user)
        if not room.can_view(user=self.request.user, profile=profile):
            raise PermissionDenied("You do not have access to this room.")
        return room


class RoomMessagesAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        room = get_object_or_404(Room, pk=self.kwargs["pk"])
        profile = ensure_user_profile(self.request.user)
        if not room.can_view(user=self.request.user, profile=profile):
            raise PermissionDenied("You do not have access to this room.")
        return Message.objects.select_related("sender", "room").filter(room=room).order_by("-created_at")
