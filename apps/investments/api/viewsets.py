from posixpath import abspath
from rest_framework import status, viewsets, views, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.clients.api.permissions import HasInvestorProfile
from apps.investments.api.serializers import InvestorCurrencySerializer
from apps.investments.repositories import InvestorCurrencyRepository
from apps.investments.services import CurrencyService
from broker.swagger import extend_schema_from_yaml


class CurrenciesView(views.APIView):
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


class InvestorCurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InvestorCurrencySerializer

    permission_classes = [IsAuthenticated, HasInvestorProfile]

    def get_queryset(self):
        queryset = InvestorCurrencyRepository.get_by_investor(
            self.request.user.investorprofile
        )
        return queryset
