from posixpath import abspath
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.commons.models import Bank
from apps.commons.api.serializers import BankSerializer
from broker.swagger import extend_schema_from_yaml


class BankViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema_from_yaml(
        abspath("apps/commons/swagger/banks/list.yml"),
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema_from_yaml(
        abspath("apps/commons/swagger/banks/get.yml"),
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
