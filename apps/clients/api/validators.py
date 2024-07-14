from decimal import Decimal
from rest_framework import serializers

from apps.clients.models import InvestorBankAccount, InvestorProfile


class UserValidator:
    def validate_passwords(self, password1: str, password2: str) -> None:
        if password1 != password2:
            raise serializers.ValidationError("Passwords are not the same.")


class BankTransactionValidator:
    def validate_bank_account_is_from_investor(
        self, bank_account: InvestorBankAccount, investor: InvestorProfile
    ) -> None:
        if bank_account.investor != investor:
            raise serializers.ValidationError("Bank account not found.")

    def validate_amount_is_not_0(self, amount: Decimal) -> None:
        zero = Decimal("0.00")
        if amount == zero:
            raise serializers.ValidationError("Amount must be different form 0.")

    def validate_has_amount_to_withdraw(
        self, investor: InvestorProfile, amount: Decimal
    ) -> None:
        zero = Decimal("0.00")
        if amount < zero and investor.amount < (amount * -1):
            raise serializers.ValidationError(
                "The customer does not have enough funds to withdraw."
            )
