from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from apps.clients.api.viewsets import (
    BankTransactionViewSet,
    InvestorBankAccountViewSet,
    InvestorProfileViewSet,
)

router = DefaultRouter()
router.register(r"users", InvestorProfileViewSet, basename="user")
router.register(r"bank_accounts", InvestorBankAccountViewSet, basename="bank_account")
router.register(
    r"bank_transactions", BankTransactionViewSet, basename="bank_transaction"
)

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
