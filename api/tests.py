from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task

User = get_user_model()


class AuthenticationAndTaskTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="StrongPass123!")
        self.client.force_authenticate(self.user)

    def test_authenticated_user_can_create_and_list_own_tasks(self):
        create = self.client.post(
            "/api/tasks/",
            {
                "title": "Test API",
                "status": "todo",
                "priority": "high",
                "category": "study",
                "due_date": "2026-10-01",
            },
            format="json",
        )
        self.assertEqual(create.status_code, status.HTTP_201_CREATED)
        listing = self.client.get("/api/tasks/")
        self.assertEqual(listing.status_code, status.HTTP_200_OK)
        self.assertEqual(len(listing.data["results"]), 1)
        self.assertEqual(listing.data["results"][0]["priority"], "high")

    def test_tasks_can_be_filtered_and_searched(self):
        Task.objects.create(owner=self.user, title="Database revision", priority="high", category="study")
        Task.objects.create(owner=self.user, title="Buy groceries", priority="low", category="personal")

        response = self.client.get("/api/tasks/?priority=high&search=database")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "Database revision")

    def test_task_list_supports_page_size(self):
        Task.objects.create(owner=self.user, title="First")
        Task.objects.create(owner=self.user, title="Second")

        response = self.client.get("/api/tasks/?page_size=1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIsNotNone(response.data["next"])

    def test_user_cannot_access_another_users_task(self):
        other = User.objects.create_user(username="other", password="StrongPass123!")
        task = Task.objects.create(owner=other, title="Private")
        response = self.client.get(f"/api/tasks/{task.pk}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_home_endpoint(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
