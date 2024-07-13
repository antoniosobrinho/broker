from apps.clients.models import InvestorBankAccount, InvestorProfile
from django.db.models.query import QuerySet


class InvestorBankAccountRepository:
    @staticmethod
    def get_accounts_for_investor(
        investor_profile: InvestorProfile,
    ) -> QuerySet[InvestorBankAccount]:
        return InvestorBankAccount.objects.filter(investor=investor_profile)
