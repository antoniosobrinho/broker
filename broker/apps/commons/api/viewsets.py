from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.commons.models import Bank
from apps.commons.api.serializers import BankSerializer


class BankViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated]
