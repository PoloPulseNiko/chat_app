from django.test import TestCase
from django.urls import reverse

from accounts_app.models import ChatUser


class ProfileTests(TestCase):
    def setUp(self):
        self.user = ChatUser.objects.create_user(
            username="niko", email="niko@example.com", password="pass12345", display_name="Niko"
        )
        self.other = ChatUser.objects.create_user(
            username="anna", email="anna@example.com", password="pass12345", display_name="Anna"
        )

    def test_profile_list_is_public(self):
        response = self.client.get(reverse("profile_list"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_profile_owner_can_edit(self):
        self.client.login(username="niko", password="pass12345")
        response = self.client.post(
            reverse("profile_edit", args=[self.user.profile.pk]),
            {"nickname": "Niko", "bio": "Updated bio"},
        )
        self.assertRedirects(response, reverse("profile_detail", args=[self.user.profile.pk]))
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, "Updated bio")

    def test_profile_non_owner_cannot_edit(self):
        self.client.login(username="anna", password="pass12345")
        response = self.client.get(reverse("profile_edit", args=[self.user.profile.pk]))
        self.assertEqual(response.status_code, 403)
