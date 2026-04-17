from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.CharField(source="recipient.nickname", read_only=True)
    actor = serializers.CharField(source="actor.nickname", read_only=True)
    room = serializers.CharField(source="room.name", read_only=True)

    class Meta:
        model = Notification
        fields = ("id", "recipient", "actor", "room", "notification_type", "text", "is_read", "created_at")

