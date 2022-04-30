from copy import deepcopy

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """Test the users public API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            "email": "test@admin.com",
            "password": "testpass",
            "name": "Berin CD",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload.get("password")))
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        """Test create user should fail if user exists"""
        payload = {
            "email": "test@admin.com",
            "password": "testpass",
            "name": "Berin CD",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 6 characters"""
        payload = {
            "email": "test@admin.com",
            "password": "pw",
            "name": "Berin CD",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model().objects.filter(email=payload.get("email")).exists()
        )
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that token is created for the user"""
        payload = {
            "email": "test@admin.com",
            "password": "testPass",
            "name": "Berin CD",
        }
        create_user(**payload)
        del payload["name"]
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test token is not created if invalid credentials are given"""
        payload = {
            "email": "test@admin.com",
            "password": "testPass",
            "name": "Berin CD",
        }
        create_user(**payload)
        del payload["name"]
        payload_copy = deepcopy(payload)
        payload_copy["password"] = "wrong_password"
        res = self.client.post(TOKEN_URL, payload_copy)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test token is not created when user does not exist"""
        payload = {
            "email": "test@admin.com",
            "password": "testPass",
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {"email": "berin@email.com"})
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
