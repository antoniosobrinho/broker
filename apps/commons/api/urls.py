from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from apps.commons.api.viewsets import BankViewSet

router = DefaultRouter()
router.register(r"banks", BankViewSet, basename="bank")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
