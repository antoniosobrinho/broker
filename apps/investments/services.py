from decimal import Decimal
from typing import Dict, List
import requests
from django.conf import settings
from django.db import transaction

from apps.clients.models import InvestorProfile
from apps.clients.services import InvestorProfileService
from apps.investments.dataclasses import PerformanceDataClass
from apps.investments.models import InvestorCurrency, InvestorTradeCurrency
from apps.investments.repositories import (
    InvestorCurrencyRepository,
    InvestorTradeCurrencyRepository,
)


class CurrencyService:
    @staticmethod
    def get_currencies_values() -> Dict[str, float]:
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

        amount_spent = quantity * currency_value * -1

        InvestorProfileService.sum_amount(investor, Decimal(amount_spent))

        return trade

    @staticmethod
    @transaction.atomic
    def sell_currency(
        currency: str, currency_value: Decimal, investor: InvestorProfile, quantity: int
    ) -> InvestorTradeCurrency:
        investor_currency = InvestorCurrencyRepository.get_investor_currency(
            investor, currency
        )
        investor_currency.quantity -= quantity
        investor_currency.save()

        amount_won = currency_value * quantity

        InvestorProfileService.sum_amount(investor, Decimal(amount_won))

        trade = InvestorTradeCurrencyRepository.create(
            currency, investor, currency_value, (quantity * -1)
        )

        return trade


class InvestorCurrencyService:
    @staticmethod
    def get_performance(investor: InvestorProfile) -> List[PerformanceDataClass]:
        try:
            currencies = CurrencyService.get_currencies_values()
        except:
            raise Exception

        investor_currencies = InvestorCurrencyRepository.get_by_investor(investor)

        performances = list()

        for investor_currency in investor_currencies:
            currency_value = currencies[investor_currency.currency]
            performances.append(
                InvestorCurrencyService.calculate_gain(
                    investor_currency, Decimal(currency_value)
                )
            )

        return performances

    @staticmethod
    def calculate_gain(
        investor_currency: InvestorCurrency, currency_value: Decimal
    ) -> PerformanceDataClass:
        pct_gain = (currency_value / investor_currency.mean_value) - 1

        total_spend = investor_currency.mean_value * investor_currency.quantity

        money_gain = total_spend * pct_gain

        current_money = total_spend + money_gain

        pct_gain *= 100

        return PerformanceDataClass(
            currency=investor_currency.currency,
            total_spend=total_spend,
            money_gain_loss=money_gain,
            current_money=current_money,
            pct=pct_gain,
        )
