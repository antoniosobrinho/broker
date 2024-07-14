from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from apps.investments.api.viewsets import (
    CurrenciesView,
    InvestorCurrencyViewSet,
    InvestorTradeCurrencyViewSet,
)


router = DefaultRouter()
router.register(
    r"investor_currencies", InvestorCurrencyViewSet, basename="investor_currencies"
)
router.register(
    r"trade_currencies", InvestorTradeCurrencyViewSet, basename="trade_currencies"
)

urlpatterns = [
    re_path(r"^", include(router.urls)),
    path("currencies/", CurrenciesView.as_view(), name="currencies"),
]
