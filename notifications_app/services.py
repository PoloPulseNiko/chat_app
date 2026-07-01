from .tasks import queue_broadcast_notifications, queue_message_notifications
from .models import Notification


def create_message_notifications(message):
    queue_message_notifications(message)

def create_direct_message_notifications(direct_message):
    recipients = direct_message.conversation.participants.exclude(pk=direct_message.sender.pk)
    notifications = [
        Notification(
            recipient=member,
            actor=direct_message.sender,
            notification_type=Notification.DIRECT_MESSAGE,
            text=f"{direct_message.sender.nickname} sent you a private message.",
            direct_message=direct_message,
        )
        for member in recipients
    ]
    if notifications:
        Notification.objects.bulk_create(notifications)


def create_room_notifications(room):
    members = room.members.exclude(pk=room.creator_id)
    notifications = [
        Notification(
            recipient=member,
            actor=room.creator,
            room=room,
            notification_type=Notification.ROOM,
            text=f"{room.creator.nickname} updated room {room.name}.",
        )
        for member in members
    ]
    if notifications:
        Notification.objects.bulk_create(notifications)


def create_broadcast_notifications(room, actor, text):
    queue_broadcast_notifications(room, actor, text)


def create_invitation_notifications(invitation):
    actor = invitation.invited_by or invitation.room.creator
    Notification.objects.update_or_create(
        recipient=invitation.invitee,
        room=invitation.room,
        notification_type=Notification.INVITE,
        defaults={
            "actor": actor,
            "text": f"{actor.nickname} invited you to join {invitation.room.name}.",
            "is_read": False,
            "message": None,
            "direct_message": None,
        },
    )
