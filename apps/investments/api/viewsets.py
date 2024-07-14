from posixpath import abspath
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.clients.api.permissions import HasInvestorProfile
from apps.investments.services import CurrencyService
from broker.swagger import extend_schema_from_yaml


class CurrenciesView(APIView):
    permission_classes = [IsAuthenticated, HasInvestorProfile]

    @extend_schema_from_yaml(
        abspath("apps/investments/swagger/currencies/get.yml"),
    )
    def get(self, request, *args, **kwargs):
        try:
            currencies = CurrencyService.get_currency_values()
            return Response(currencies, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": "Try again latter"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
