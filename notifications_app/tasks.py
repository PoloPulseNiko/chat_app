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


async def _create_room_notifications(room):
    room_members = await sync_to_async(list)(room.members.exclude(pk=room.creator.pk))
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


def queue_room_notifications(room):
    _run_background(_create_room_notifications(room))


def queue_broadcast_notifications(room, actor, text):
    _run_background(_create_broadcast_notifications(room, actor, text))

