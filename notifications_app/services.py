from .tasks import queue_broadcast_notifications, queue_message_notifications, queue_room_notifications


def create_message_notifications(message):
    queue_message_notifications(message)


def create_room_notifications(room):
    queue_room_notifications(room)


def create_broadcast_notifications(room, actor, text):
    queue_broadcast_notifications(room, actor, text)
