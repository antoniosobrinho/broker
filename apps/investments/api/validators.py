from rest_framework import serializers

from apps.clients.models import InvestorProfile
from apps.investments.repositories import InvestorCurrencyRepository


class InvestorTradeCurrencyValidator:
    def validate_currency_exists(self, currency: str, currencies: dict) -> None:
        if currency not in currencies:
            raise serializers.ValidationError("Currency does not exists.")

    def validate_quantity_is_not_zero(self, quantity: int) -> None:
        if quantity == 0:
            raise serializers.ValidationError("Quantity must be different from zero.")

    def validate_has_funds_to_buy(
        self, investor: InvestorProfile, currency: str, quantity: int, currencies: dict
    ) -> None:
        if quantity > 0:
            currency_value = currencies[currency]
            total_value = currency_value * quantity

            if investor.amount < total_value:
                raise serializers.ValidationError(
                    "You don't have enough funds for that amount."
                )

    def validate_has_currency_to_sell(
        self, investor: InvestorProfile, currency: str, quantity: int
    ) -> None:
        if quantity < 0:
            investor_currency = InvestorCurrencyRepository.get_investor_currency(
                investor, currency
            )
            if not investor_currency:
                raise serializers.ValidationError(
                    "You don't have that currency to sell."
                )

            if investor_currency.quantity < (quantity * -1):
                raise serializers.ValidationError("You don't have enough to sell.")
