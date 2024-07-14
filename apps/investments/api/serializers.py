from rest_framework import serializers

from apps.investments.models import InvestorCurrency


class InvestorCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorCurrency
        fields = ["currency", "mean_value"]
        read_only_fields = ["mean_value"]
