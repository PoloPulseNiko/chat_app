from django.test import TestCase
from django.urls import reverse

from accounts_app.models import ChatUser
from messages_app.models import Message

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
        response = self.client.get(reverse("room_list"), {"category": self.category.pk}, secure=True)
        self.assertContains(response, "Django Room")

    def test_room_list_does_not_duplicate_rooms(self):
        self.room.members.add(self.member.profile)
        self.client.login(username="member", password="pass12345")
        response = self.client.get(reverse("room_list"), secure=True)
        self.assertEqual(response.content.decode().count("Django Room"), 1)

    def test_room_create_adds_owner_membership(self):
        self.client.login(username="member", password="pass12345")
        response = self.client.post(
            reverse("room_create"),
            {"name": "New Room", "description": "Hello room", "category": self.category.pk, "tags": [self.tag.pk]},
            secure=True,
        )
        self.assertRedirects(response, reverse("room_list"))
        room = Room.objects.get(name="New Room")
        self.assertTrue(room.members.filter(pk=self.member.profile.pk).exists())
        self.assertTrue(Membership.objects.filter(profile=self.member.profile, room=room).exists())

    def test_room_join_adds_membership(self):
        self.client.login(username="member", password="pass12345")
        response = self.client.post(reverse("room_join", args=[self.room.pk]), secure=True)
        self.assertRedirects(response, reverse("room_detail", args=[self.room.pk]))
        self.assertTrue(self.room.members.filter(pk=self.member.profile.pk).exists())

    def test_room_owner_can_toggle_join_policy(self):
        self.client.login(username="owner", password="pass12345")
        form_response = self.client.get(reverse("room_edit", args=[self.room.pk]), secure=True)
        self.assertContains(form_response, "Join Policy")
        response = self.client.post(
            reverse("room_edit", args=[self.room.pk]),
            {
                "name": self.room.name,
                "description": self.room.description,
                "category": self.category.pk,
                "tags": [self.tag.pk],
                "join_policy": Room.JOIN_INVITE,
            },
            secure=True,
        )
        self.assertRedirects(response, reverse("room_detail", args=[self.room.pk]), fetch_redirect_response=False)
        self.room.refresh_from_db()
        self.assertEqual(self.room.join_policy, Room.JOIN_INVITE)

    def test_inviting_someone_does_not_change_join_policy(self):
        self.room.join_policy = Room.JOIN_OPEN
        self.room.save(update_fields=["join_policy"])
        self.client.login(username="owner", password="pass12345")
        response = self.client.post(
            reverse("room_invite", args=[self.room.pk]),
            {"invitee": self.member.profile.pk},
            secure=True,
        )
        self.assertRedirects(response, reverse("room_detail", args=[self.room.pk]), fetch_redirect_response=False)
        self.room.refresh_from_db()
        self.assertEqual(self.room.join_policy, Room.JOIN_OPEN)

    def test_non_member_cannot_see_room_messages(self):
        Message.objects.create(sender=self.owner.profile, room=self.room, text="Secret room text")
        self.client.login(username="member", password="pass12345")
        response = self.client.get(reverse("room_detail", args=[self.room.pk]), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Room content is members only")
        self.assertNotContains(response, "Secret room text")

    def test_non_owner_cannot_edit_room(self):
        self.client.login(username="member", password="pass12345")
        response = self.client.get(reverse("room_edit", args=[self.room.pk]), secure=True)
        self.assertEqual(response.status_code, 403)

    def test_non_member_cannot_post_message(self):
        self.client.login(username="member", password="pass12345")
        response = self.client.post(reverse("room_detail", args=[self.room.pk]), {"text": "Hello"}, secure=True)
        self.assertRedirects(response, reverse("room_detail", args=[self.room.pk]), fetch_redirect_response=False)
        self.assertEqual(self.room.messages.count(), 0)

    def test_room_api_returns_room_data(self):
        response = self.client.get(reverse("api_room_list"), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "Django Room")
