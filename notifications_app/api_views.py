from rest_framework import generics, permissions

from accounts_app.services import ensure_user_profile

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile = ensure_user_profile(self.request.user)
        return Notification.objects.select_related("recipient", "actor", "room").filter(
            recipient=profile
        )
