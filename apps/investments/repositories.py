from decimal import Decimal
from typing import Optional
from apps.clients.models import InvestorProfile
from django.db.models.query import QuerySet

from apps.investments.models import InvestorCurrency, InvestorTradeCurrency


class InvestorCurrencyRepository:
    @staticmethod
    def get_by_investor(investor: InvestorProfile) -> QuerySet[InvestorCurrency]:
        return InvestorCurrency.objects.filter(investor=investor)

    @staticmethod
    def get_investor_currency(
        investor: InvestorProfile, currency: str
    ) -> Optional[InvestorCurrency]:
        currency = InvestorCurrency.objects.filter(investor=investor, currency=currency)
        if currency:
            return currency
        return None

    @staticmethod
    def create(
        currency: str, investor: InvestorProfile, mean_value: Decimal, quantity: int
    ) -> InvestorCurrency:
        investor_currency = InvestorCurrency.objects.create(
            currency=currency,
            investor=investor,
            mean_value=mean_value,
            quantity=quantity,
        )


class InvestorTradeCurrencyRepository:
    @staticmethod
    def create(
        currency: str, investor: InvestorProfile, unit_value: Decimal, quantity: int
    ) -> InvestorTradeCurrency:
        trade = InvestorTradeCurrency.objects.create(
            currency=currency,
            investor=investor,
            unit_value=unit_value,
            quantity=quantity,
        )

        return trade
