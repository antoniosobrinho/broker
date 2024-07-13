from posixpath import abspath
from rest_framework import viewsets, mixins
from apps.clients.api.serializers import InvestorProfileSerializer
from broker.swagger import extend_schema_from_yaml


class InvestorProfileViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = InvestorProfileSerializer
    permission_classes = []
