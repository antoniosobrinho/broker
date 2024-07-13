from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.clients.api.permissions import HasInvestorProfile
from apps.clients.api.serializers import (
    InvestorBankAccountSerializer,
    InvestorProfileSerializer,
)
from apps.clients.repositories import InvestorBankAccountRepository


class InvestorProfileViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = InvestorProfileSerializer
    permission_classes = []


class InvestorBankAccountViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, HasInvestorProfile]
    serializer_class = InvestorBankAccountSerializer

    def get_queryset(self):
        queryset = InvestorBankAccountRepository.get_accounts_for_investor(
            self.request.user.investorprofile
        )
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        data["investor"] = request.user.investorprofile.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
