from rest_framework import serializers


class UserValidator:
    def validate_passwords(password1: str, password2: str) -> None:
        if password1 != password2:
            raise serializers.ValidationError("Passwords are not the same.")
