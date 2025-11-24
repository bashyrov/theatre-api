from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

class UserTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="password",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_patch_user(self):

        payload = {
            "email": f"test{self.user}"
        }
        response_user = self.client.patch(reverse("users:manage"), payload)

        self.assertEqual(response_user.status_code, status.HTTP_200_OK)
