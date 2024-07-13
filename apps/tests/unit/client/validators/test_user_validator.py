from django.test import TestCase
from rest_framework.serializers import ValidationError
from apps.clients.api.validators import UserValidator


class UserValidatorTest(TestCase):

    def test_validate_passwords_match(self):
        password1 = "password123"
        password2 = "password123"
        try:
            UserValidator().validate_passwords(password1, password2)
        except ValidationError:
            self.fail("validate_passwords() raised ValidationError unexpectedly!")

    def test_validate_passwords_do_not_match_should_raise_validation_error(self):
        password1 = "password123"
        password2 = "differentpassword"
        with self.assertRaises(ValidationError):
            UserValidator().validate_passwords(password1, password2)
