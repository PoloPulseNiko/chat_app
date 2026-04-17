from django.test import TestCase
from django.urls import reverse

from accounts_app.models import ChatUser
from profiles_app.models import Profile
from rooms_app.models import Room

from .models import Notification


class NotificationTests(TestCase):
    def setUp(self):
        self.user = ChatUser.objects.create_user(
            username="niko", email="niko@example.com", password="pass12345", display_name="Niko"
        )
        self.other = ChatUser.objects.create_user(
            username="anna", email="anna@example.com", password="pass12345", display_name="Anna"
        )
        self.room = Room.objects.create(name="Django", description="Talk", creator=self.user.profile)
        self.room.members.add(self.user.profile, self.other.profile)
        self.notification = Notification.objects.create(
            recipient=self.user.profile,
            actor=self.other.profile,
            room=self.room,
            notification_type=Notification.MESSAGE,
            text="Anna posted in Django.",
        )

    def test_notification_list_requires_login(self):
        response = self.client.get(reverse("notification_list"))
        self.assertEqual(response.status_code, 302)

    def test_mark_read_updates_notification(self):
        self.client.login(username="niko", password="pass12345")
        response = self.client.post(reverse("notification_mark_read", args=[self.notification.pk]))
        self.assertRedirects(response, reverse("notification_list"))
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    def test_notification_filter_unread_only(self):
        Notification.objects.create(
            recipient=self.user.profile,
            actor=self.other.profile,
            room=self.room,
            notification_type=Notification.ROOM,
            text="Room updated.",
            is_read=True,
        )
        self.client.login(username="niko", password="pass12345")
        response = self.client.get(reverse("notification_list"), {"unread_only": "on"})
        notifications = response.context["notifications"]
        self.assertEqual(notifications.count(), 1)

    def test_notification_api_requires_login(self):
        response = self.client.get(reverse("api_notification_list"))
        self.assertEqual(response.status_code, 403)

    def test_notification_api_returns_user_notifications(self):
        self.client.login(username="niko", password="pass12345")
        response = self.client.get(reverse("api_notification_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

