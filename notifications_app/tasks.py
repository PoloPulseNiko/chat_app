import asyncio
import threading

from asgiref.sync import sync_to_async

from .models import Notification


async def _create_message_notifications(message):
    room_members = await sync_to_async(list)(message.room.members.exclude(pk=message.sender.pk))
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
        await sync_to_async(Notification.objects.bulk_create)(notifications)


async def _create_direct_message_notifications(direct_message):
    recipients = await sync_to_async(list)(direct_message.conversation.participants.exclude(pk=direct_message.sender.pk))
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
        await sync_to_async(Notification.objects.bulk_create)(notifications)


async def _create_invitation_notifications(invitation):
    actor = invitation.invited_by or invitation.room.creator
    notification_text = f"{actor.nickname} invited you to join {invitation.room.name}."
    await sync_to_async(Notification.objects.update_or_create)(
        recipient=invitation.invitee,
        room=invitation.room,
        notification_type=Notification.INVITE,
        defaults={
            "actor": actor,
            "text": notification_text,
            "is_read": False,
            "message": None,
            "direct_message": None,
        },
    )


async def _create_room_notifications(room):
    creator = await sync_to_async(lambda: room.creator)()
    room_members = await sync_to_async(list)(room.members.exclude(pk=room.creator_id))
    notifications = [
        Notification(
            recipient=member,
            actor=creator,
            room=room,
            notification_type=Notification.ROOM,
            text=f"{creator.nickname} updated room {room.name}.",
        )
        for member in room_members
    ]
    if notifications:
        await sync_to_async(Notification.objects.bulk_create)(notifications)


async def _create_broadcast_notifications(room, actor, text):
    room_members = await sync_to_async(list)(room.members.exclude(pk=actor.pk))
    notifications = [
        Notification(
            recipient=member,
            actor=actor,
            room=room,
            notification_type=Notification.ROOM,
            text=text,
        )
        for member in room_members
    ]
    if notifications:
        await sync_to_async(Notification.objects.bulk_create)(notifications)


def _run_background(coroutine):
    thread = threading.Thread(target=lambda: asyncio.run(coroutine), daemon=True)
    thread.start()


def queue_message_notifications(message):
    _run_background(_create_message_notifications(message))


def queue_direct_message_notifications(direct_message):
    _run_background(_create_direct_message_notifications(direct_message))


def queue_invitation_notifications(invitation):
    _run_background(_create_invitation_notifications(invitation))


def queue_room_notifications(room):
    _run_background(_create_room_notifications(room))


def queue_broadcast_notifications(room, actor, text):
    _run_background(_create_broadcast_notifications(room, actor, text))
