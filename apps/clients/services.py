from decimal import Decimal
from django.db import transaction
from apps.clients.models import (
    BankTransaction,
    InvestorBankAccount,
    InvestorProfile,
    User,
)


class UserService:
    @staticmethod
    def create_user(username: str, email: str, password: str) -> User:
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        return user


class InvestorProfileService:
    @staticmethod
    def sum_amount(
        investor_profile: InvestorProfile, amount: Decimal
    ) -> InvestorProfile:
        investor_profile.amount += amount
        investor_profile.save()

        return investor_profile


class BankTransactionService:
    @staticmethod
    @transaction.atomic
    def create_bank_transaction(
        bank_account: InvestorBankAccount, amount: Decimal
    ) -> BankTransaction:
        InvestorProfileService.sum_amount(bank_account.investor, amount)

        bank_transaction = BankTransaction.objects.create(
            bank_account=bank_account, amount=amount
        )
        return bank_transaction
