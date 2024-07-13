from rest_framework import serializers
from apps.clients.api.validators import UserValidator
from apps.clients.models import User, InvestorProfile


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def validate(self, attrs: dict):
        attrs = super().validate(attrs)

        user_validator = UserValidator()
        user_validator.validate_passwords(
            attrs.get("password1"), attrs.get("password2")
        )

        return attrs

    def create(self, validated_data: dict) -> User:
        password = validated_data.pop("password1")
        validated_data.pop("password2")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class InvestorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = InvestorProfile
        fields = ["user", "birth_date", "address"]

    def create(self, validated_data) -> InvestorProfile:
        user_data = validated_data.pop("user")
        user = UserSerializer().create(user_data)

        investor_profile = InvestorProfile.objects.create(user=user, **validated_data)

        return investor_profile
