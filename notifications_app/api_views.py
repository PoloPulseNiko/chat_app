from rest_framework import generics, permissions

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.select_related("recipient", "actor", "room").filter(
            recipient=self.request.user.profile
        )

