from decimal import Decimal
from typing import Dict
import requests
from django.conf import settings
from django.db import transaction

from apps.clients.models import InvestorProfile
from apps.clients.services import InvestorProfileService
from apps.investments.models import InvestorTradeCurrency
from apps.investments.repositories import (
    InvestorCurrencyRepository,
    InvestorTradeCurrencyRepository,
)


class CurrencyService:
    @staticmethod
    def get_currency_values() -> Dict[str, float]:
        url = settings.EXCHANGERATESAPI_HOST

        params = {"access_key": settings.EXCHANGERATESAPI_KEY}

        response = requests.get(url, params=params)

        if response.status_code == 200:
            currencies = response.json()["rates"]
            return currencies

        raise Exception()


class InvestorTradeCurrencyService:
    @staticmethod
    @transaction.atomic
    def buy_currency(
        currency: str, currency_value: Decimal, investor: InvestorProfile, quantity: int
    ) -> InvestorTradeCurrency:
        trade = InvestorTradeCurrencyRepository.create(
            currency, investor, currency_value, quantity
        )

        investor_currency = InvestorCurrencyRepository.get_investor_currency(
            investor, currency
        )

        if investor_currency:
            total_value = (
                investor_currency.quantity * investor_currency.mean_value
            ) + (quantity * currency_value)
            total_quantity = investor_currency.quantity + quantity
            mean_value = total_value / total_quantity

            investor_currency.quantity += quantity
            investor_currency.mean_value = mean_value
            investor_currency.save()
        else:
            InvestorCurrencyRepository.create(
                currency, investor, currency_value, quantity
            )

        total = quantity * currency_value * -1

        InvestorProfileService.sum_amount(investor, Decimal(total))

        return trade
