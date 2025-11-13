from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from auth_api.models import User  # import your user model

class LoginViewTestCase(APITestCase):
    def setUp(self):
        # Create a tests user
        self.user = User.objects.create(
            email="tests@example.com",
            password="test1234",
            is_active=True
        )
        self.url = reverse("api/auth/login")  # your URL name from urls.py

    def test_login_success(self):
        data = {
            "email": "tests@example.com",
            "password": "test1234"
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["message"], "You are logged in successfully")

    def test_login_invalid_password(self):
        data = {
            "email": "tests@example.com",
            "password": "wrongpass"
        }
        response = self.client.post(self.url, data, format="json")

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("error", response.data)

    def test_login_missing_fields(self):
        data = {
            "email": ""
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
