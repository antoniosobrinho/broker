from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from apps.clients.api.viewsets import InvestorBankAccountViewSet, InvestorProfileViewSet

router = DefaultRouter()
router.register(r"user", InvestorProfileViewSet, basename="user")
router.register(r"bank_account", InvestorBankAccountViewSet, basename="bank_account")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
