from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from .models import ChatUser


class AccountsTests(TestCase):
    def test_signup_creates_user_and_profile(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "niko",
                "email": "niko@example.com",
                "display_name": "Niko",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("room_list"))
        user = ChatUser.objects.get(username="niko")
        self.assertEqual(user.profile.nickname, "Niko")

    def test_default_groups_exist(self):
        self.assertTrue(Group.objects.filter(name="Moderators").exists())
        self.assertTrue(Group.objects.filter(name="Room Managers").exists())

