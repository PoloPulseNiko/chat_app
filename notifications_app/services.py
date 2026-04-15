from .models import Notification


def create_message_notifications(message):
    room_members = message.room.members.exclude(pk=message.sender.pk)
    notifications = [
        Notification(
            recipient=member,
            actor=message.sender,
            room=message.room,
            message=message,
            notification_type=Notification.MESSAGE,
            text=f"{message.sender.nickname} posted in {message.room.name}.",
        )
        for member in room_members
    ]

    if notifications:
        Notification.objects.bulk_create(notifications)


def create_room_notifications(room):
    room_members = room.members.exclude(pk=room.creator.pk)
    notifications = [
        Notification(
            recipient=member,
            actor=room.creator,
            room=room,
            notification_type=Notification.ROOM,
            text=f"{room.creator.nickname} updated room {room.name}.",
        )
        for member in room_members
    ]

    if notifications:
        Notification.objects.bulk_create(notifications)

