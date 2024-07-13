# permissions.py

from rest_framework.permissions import BasePermission


class HasInvestorProfile(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "investorprofile")
