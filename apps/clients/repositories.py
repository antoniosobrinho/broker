from apps.clients.models import BankTransaction, InvestorBankAccount, InvestorProfile
from django.db.models.query import QuerySet


class InvestorBankAccountRepository:
    @staticmethod
    def get_accounts_for_investor(
        investor_profile: InvestorProfile,
    ) -> QuerySet[InvestorBankAccount]:
        return InvestorBankAccount.objects.filter(investor=investor_profile)


class BankTransactionRepository:
    @staticmethod
    def get_bank_transactions_from_investor(
        investor_profile: InvestorProfile,
    ) -> QuerySet[BankTransaction]:
        return BankTransaction.objects.filter(bank_account__investor=investor_profile)
