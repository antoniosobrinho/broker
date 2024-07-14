from rest_framework import serializers
from apps.clients.api.validators import BankTransactionValidator, UserValidator
from apps.clients.models import (
    BankTransaction,
    InvestorBankAccount,
    User,
    InvestorProfile,
)
from apps.clients.services import (
    BankTransactionService,
    UserService,
)
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def validate(self, attrs: dict):
        attrs = super().validate(attrs)

        user_validator = UserValidator()
        user_validator.validate_passwords(attrs["password1"], attrs["password2"])

        return attrs

    @transaction.atomic
    def create(self, validated_data: dict) -> User:
        user = UserService.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password1"],
        )

        return user


class InvestorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = InvestorProfile
        fields = ["user", "birth_date", "address"]

    @transaction.atomic
    def create(self, validated_data) -> InvestorProfile:
        user_data = validated_data.pop("user")
        user = UserSerializer().create(user_data)

        investor_profile = InvestorProfile.objects.create(user=user, **validated_data)

        return investor_profile


class InvestorBankAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestorBankAccount
        fields = ["id", "investor", "bank", "account_number"]
        extra_kwargs = {"investor": {"write_only": True}}


class BankTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankTransaction
        fields = ["id", "amount", "bank_account", "created_at"]
        read_only_fields = ["created_at"]

    def validate(self, attrs):
        attrs = super().validate(attrs)

        investor = self.context["request"].user.investorprofile

        bank_transaction_validator = BankTransactionValidator()

        bank_transaction_validator.validate_bank_account_is_from_investor(
            attrs["bank_account"], investor
        )
        bank_transaction_validator.validate_amount_is_not_0(attrs["amount"])
        bank_transaction_validator.validate_has_amount_to_withdraw(
            investor, attrs["amount"]
        )
        return attrs

    def create(self, validated_data):
        bank_account = validated_data["bank_account"]
        amount = validated_data["amount"]

        bank_transaction = BankTransactionService.create_bank_transaction(
            bank_account=bank_account, amount=amount
        )

        return bank_transaction
