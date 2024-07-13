from unittest.mock import Mock, patch
from django.test import TestCase
from apps.clients.api.serializers import UserSerializer
from apps.clients.services import UserService


class UserSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "password123",
            "password2": "password123",
        }

    @patch("apps.clients.api.validators.UserValidator.validate_passwords")
    def test_validate_passwords_called(self, mock_validate_passwords):
        serializer = UserSerializer(data=self.data)

        is_valid = serializer.is_valid()

        self.assertTrue(is_valid)

        mock_validate_passwords.assert_called_once_with(
            self.data["password1"], self.data["password2"]
        )

    def test_is_valid_with_missing_username(self):
        data = self.data
        del data["username"]

        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["username"][0], "This field is required.")

    def test_is_valid_with_missing_email(self):
        data = self.data
        del data["email"]

        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["email"][0], "This field is required.")

    def test_is_valid_with_missing_password1(self):
        data = self.data
        del data["password1"]

        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["password1"][0], "This field is required.")

    def test_is_valid_with_missing_password2(self):
        data = self.data
        del data["password2"]

        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["password2"][0], "This field is required.")

    @patch.object(UserService, "create_user")
    def test_create_user(self, create_user):
        user = Mock()
        create_user.return_value = user

        result = UserSerializer(data=self.data).create(self.data)

        create_user.assert_called_once_with(
            "testuser", "testuser@example.com", "password123"
        )

        self.assertEqual(result, user)
