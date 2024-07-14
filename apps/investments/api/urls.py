from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from apps.investments.api.viewsets import CurrenciesView


router = DefaultRouter()

urlpatterns = [
    re_path(r"^", include(router.urls)),
    path("currencies/", CurrenciesView.as_view(), name="currencies"),
]
