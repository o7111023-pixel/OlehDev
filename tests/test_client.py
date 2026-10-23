from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from olehdev.models import ProjectRequest


class ClientDashboardTests(TestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(
            username="client1",
            password="test-password-123",
        )
        self.other_user = User.objects.create_user(
            username="client2",
            password="test-password-123",
        )

        self.project_request = ProjectRequest.objects.create(
            user=self.client_user,
            name="Portfolio website",
            email="client1@example.com",
            description="Create a portfolio website",
        )

    def test_anonymous_user_cannot_access_dashboard(self):
        response = self.client.get(reverse("client_dashboard"))

        self.assertEqual(response.status_code, 302)

    def test_client_can_access_dashboard(self):
        self.client.login(
            username="client1",
            password="test-password-123",
        )

        response = self.client.get(reverse("client_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Portfolio website")

    def test_client_can_open_own_request(self):
        self.client.login(
            username="client1",
            password="test-password-123",
        )

        response = self.client.get(
            reverse(
                "client_request_detail",
                kwargs={"request_id": self.project_request.id},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create a portfolio website")

    def test_client_cannot_open_another_users_request(self):
        self.client.login(
            username="client2",
            password="test-password-123",
        )

        response = self.client.get(
            reverse(
                "client_request_detail",
                kwargs={"request_id": self.project_request.id},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_client_can_cancel_own_request(self):
        self.client.login(
            username="client1",
            password="test-password-123",
        )

        response = self.client.post(
            reverse(
                "client_cancel_request",
                kwargs={"request_id": self.project_request.id},
            )
        )

        self.project_request.refresh_from_db()

        self.assertRedirects(
            response,
            reverse(
                "client_request_detail",
                kwargs={"request_id": self.project_request.id},
            ),
        )
        self.assertEqual(
            self.project_request.status,
            ProjectRequest.Status.CANCELLED,
        )
