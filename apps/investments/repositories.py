from apps.clients.models import InvestorProfile
from django.db.models.query import QuerySet

from apps.investments.models import InvestorCurrency


class InvestorCurrencyRepository:
    @staticmethod
    def get_by_investor(investor: InvestorProfile) -> QuerySet[InvestorCurrency]:
        return InvestorCurrency.objects.filter(investor=investor)
