from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from olehdev.models import ProjectRequest


class AdminRequestTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin1",
            password="test-password-123",
            is_staff=True,
        )
        self.client_user = User.objects.create_user(
            username="client1",
            password="test-password-123",
        )

        self.project_request = ProjectRequest.objects.create(
            user=self.client_user,
            name="Video project",
            email="client1@example.com",
            description="Create a promotional video",
        )

    def test_anonymous_user_cannot_access_admin_requests(self):
        response = self.client.get(reverse("admin_requests"))

        self.assertEqual(response.status_code, 302)

    def test_regular_user_cannot_access_admin_requests(self):
        self.client.login(
            username="client1",
            password="test-password-123",
        )

        response = self.client.get(reverse("admin_requests"))

        self.assertEqual(response.status_code, 302)

    def test_admin_can_access_requests(self):
        self.client.login(
            username="admin1",
            password="test-password-123",
        )

        response = self.client.get(reverse("admin_requests"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Video project")

    def test_admin_can_open_request_detail(self):
        self.client.login(
            username="admin1",
            password="test-password-123",
        )

        response = self.client.get(
            reverse(
                "admin_request_detail",
                kwargs={"request_id": self.project_request.id},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create a promotional video")

    def test_regular_user_cannot_delete_request(self):
        self.client.login(
            username="client1",
            password="test-password-123",
        )

        response = self.client.post(
            reverse(
                "admin_delete_request",
                kwargs={"request_id": self.project_request.id},
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ProjectRequest.objects.filter(
                id=self.project_request.id
            ).exists()
        )

    def test_admin_can_delete_request(self):
        self.client.login(
            username="admin1",
            password="test-password-123",
        )

        response = self.client.post(
            reverse(
                "admin_delete_request",
                kwargs={"request_id": self.project_request.id},
            )
        )

        self.assertRedirects(
            response,
            reverse("admin_requests"),
        )
        self.assertFalse(
            ProjectRequest.objects.filter(
                id=self.project_request.id
            ).exists()
        )
