from django.test import TestCase
from django.urls import reverse

from accounts_app.models import ChatUser
from rooms_app.models import Room

from .models import Message, Reaction


class MessageTests(TestCase):
    def setUp(self):
        self.author = ChatUser.objects.create_user(
            username="author", email="author@example.com", password="pass12345", display_name="Author"
        )
        self.other = ChatUser.objects.create_user(
            username="other", email="other@example.com", password="pass12345", display_name="Other"
        )
        self.room = Room.objects.create(name="General", description="General room", creator=self.author.profile)
        self.room.members.add(self.author.profile, self.other.profile)
        self.message = Message.objects.create(sender=self.author.profile, room=self.room, text="Hello there")

    def test_author_can_edit_message(self):
        self.client.login(username="author", password="pass12345")
        response = self.client.post(reverse("message_edit", args=[self.message.pk]), {"text": "Edited"})
        self.assertRedirects(response, reverse("room_detail", args=[self.room.pk]))
        self.message.refresh_from_db()
        self.assertEqual(self.message.text, "Edited")

    def test_non_author_cannot_edit_message(self):
        self.client.login(username="other", password="pass12345")
        response = self.client.get(reverse("message_edit", args=[self.message.pk]))
        self.assertEqual(response.status_code, 403)

    def test_reaction_toggle_creates_reaction(self):
        self.client.login(username="other", password="pass12345")
        self.client.post(reverse("message_react", args=[self.message.pk, "like"]))
        self.assertTrue(Reaction.objects.filter(message=self.message, profile=self.other.profile, reaction_type="like").exists())

    def test_reaction_toggle_removes_existing_reaction(self):
        Reaction.objects.create(message=self.message, profile=self.other.profile, reaction_type="like")
        self.client.login(username="other", password="pass12345")
        self.client.post(reverse("message_react", args=[self.message.pk, "like"]))
        self.assertFalse(Reaction.objects.filter(message=self.message, profile=self.other.profile, reaction_type="like").exists())
