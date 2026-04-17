from django.test import TestCase
from django.urls import reverse

from accounts_app.models import ChatUser


class StaffPanelTests(TestCase):
    def setUp(self):
        self.staff_user = ChatUser.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="pass12345",
            display_name="Staff",
            is_staff=True,
        )
        self.regular_user = ChatUser.objects.create_user(
            username="regular",
            email="regular@example.com",
            password="pass12345",
            display_name="Regular",
        )

    def test_staff_dashboard_denies_regular_user(self):
        self.client.login(username="regular", password="pass12345")
        response = self.client.get(reverse("staff_dashboard"))
        self.assertEqual(response.status_code, 403)

    def test_staff_dashboard_allows_staff_user(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("staff_dashboard"))
        self.assertEqual(response.status_code, 200)

