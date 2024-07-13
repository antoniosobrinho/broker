from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from apps.clients.api.viewsets import InvestorProfileViewSet

router = DefaultRouter()
router.register(r"user", InvestorProfileViewSet, basename="user")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
