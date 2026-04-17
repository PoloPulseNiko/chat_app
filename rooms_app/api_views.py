from rest_framework import generics, permissions

from messages_app.models import Message

from .models import Room
from .serializers import MessageSerializer, RoomSerializer


class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.select_related("creator", "category").prefetch_related("tags", "members")
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]


class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.select_related("creator", "category").prefetch_related("tags", "members")
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]


class RoomMessagesAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Message.objects.select_related("sender", "room").filter(room_id=self.kwargs["pk"]).order_by("-created_at")

