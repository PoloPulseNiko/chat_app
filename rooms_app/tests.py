from django.test import TestCase
from django.urls import reverse

from accounts_app.models import ChatUser

from .models import Category, Membership, Room, Tag


class RoomTests(TestCase):
    def setUp(self):
        self.owner = ChatUser.objects.create_user(
            username="owner", email="owner@example.com", password="pass12345", display_name="Owner"
        )
        self.member = ChatUser.objects.create_user(
            username="member", email="member@example.com", password="pass12345", display_name="Member"
        )
        self.category = Category.objects.create(name="Python")
        self.tag = Tag.objects.create(name="backend")
        self.room = Room.objects.create(name="Django Room", description="Discuss Django", creator=self.owner.profile, category=self.category)
        self.room.tags.add(self.tag)
        self.room.members.add(self.owner.profile)

    def test_room_list_filter_by_category(self):
        response = self.client.get(reverse("room_list"), {"category": self.category.pk})
        self.assertContains(response, "Django Room")

    def test_room_create_adds_owner_membership(self):
        self.client.login(username="member", password="pass12345")
        response = self.client.post(
            reverse("room_create"),
            {"name": "New Room", "description": "Hello room", "category": self.category.pk, "tags": [self.tag.pk]},
        )
        self.assertRedirects(response, reverse("room_list"))
        room = Room.objects.get(name="New Room")
        self.assertTrue(room.members.filter(pk=self.member.profile.pk).exists())
        self.assertTrue(Membership.objects.filter(profile=self.member.profile, room=room).exists())

    def test_room_join_adds_membership(self):
        self.client.login(username="member", password="pass12345")
        response = self.client.post(reverse("room_join", args=[self.room.pk]))
        self.assertRedirects(response, reverse("room_detail", args=[self.room.pk]))
        self.assertTrue(self.room.members.filter(pk=self.member.profile.pk).exists())

    def test_non_owner_cannot_edit_room(self):
        self.client.login(username="member", password="pass12345")
        response = self.client.get(reverse("room_edit", args=[self.room.pk]))
        self.assertEqual(response.status_code, 403)

    def test_non_member_cannot_post_message(self):
        self.client.login(username="member", password="pass12345")
        response = self.client.post(reverse("room_detail", args=[self.room.pk]), {"text": "Hello"})
        self.assertRedirects(response, reverse("room_detail", args=[self.room.pk]))
        self.assertEqual(self.room.messages.count(), 0)

    def test_room_api_returns_room_data(self):
        response = self.client.get(reverse("api_room_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "Django Room")
