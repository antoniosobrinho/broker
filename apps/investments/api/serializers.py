from rest_framework import serializers

from apps.investments.api.validators import InvestorTradeCurrencyValidator
from apps.investments.models import InvestorCurrency, InvestorTradeCurrency
from apps.investments.services import InvestorTradeCurrencyService


class InvestorCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorCurrency
        fields = ["currency", "mean_value"]
        read_only_fields = ["mean_value"]


class InvestorTradeCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorTradeCurrency
        fields = ["currency", "unit_value", "quantity"]
        read_only_fields = ["unit_value"]

    def validate(self, attrs):
        attrs = super().validate(attrs)

        investor = self.context["request"].user.investorprofile
        currencies = self.context["currencies"]

        validators = InvestorTradeCurrencyValidator()
        validators.validate_currency_exists(attrs["currency"], currencies)
        validators.validate_quantity_is_not_zero(attrs["quantity"])
        validators.validate_has_funds_to_buy(
            investor, attrs["currency"], attrs["quantity"], currencies
        )
        validators.validate_has_currency_to_sell(
            investor, attrs["currency"], attrs["quantity"]
        )

        return attrs

    def create(self, validated_data):
        currency = validated_data["currency"]
        currency_value = self.context["currencies"][currency]
        investor = self.context["request"].user.investorprofile
        quantity = validated_data["quantity"]

        if quantity > 0:
            trade = InvestorTradeCurrencyService.buy_currency(
                currency, currency_value, investor, quantity
            )

        return trade
