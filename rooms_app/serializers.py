from rest_framework import serializers

from messages_app.models import Message

from .models import Room, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class RoomSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source="creator.nickname", read_only=True)
    category = serializers.CharField(source="category.name", read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    members_count = serializers.IntegerField(source="members.count", read_only=True)

    class Meta:
        model = Room
        fields = ("id", "name", "description", "creator", "category", "tags", "members_count")


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source="sender.nickname", read_only=True)
    room = serializers.CharField(source="room.name", read_only=True)

    class Meta:
        model = Message
        fields = ("id", "sender", "room", "text", "created_at")

