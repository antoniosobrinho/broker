from unittest.mock import Mock, patch
from django.test import TestCase
from apps.client.api.serializers import UserSerializer


class UserSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "password123",
            "password2": "password123",
        }

    @patch("apps.client.api.validators.UserValidator.validate_passwords")
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

    @patch("apps.client.api.serializers.User")
    def test_create_user(self, mock_user):
        set_password = Mock()

        save = Mock()

        user_obj = Mock()
        user_obj.set_password = set_password
        user_obj.save = save

        mock_user.return_value = user_obj

        serializer = UserSerializer(data=self.data)

        user = serializer.create(self.data)

        mock_user.assert_called_once_with(
            **{"username": "testuser", "email": "testuser@example.com"}
        )
        set_password.assert_called_once_with("password123")
        save.assert_called_once_with()

        self.assertEqual(user, user_obj)
