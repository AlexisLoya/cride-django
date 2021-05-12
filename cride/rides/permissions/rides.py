"""Rides permissions."""
from rest_framework.permissions import BasePermission


class IsRideOwner(BasePermission):
    """Verify requesting user is the ride owner"""

    def has_object_permission(self, request, view, obj):
        """Verify request user is the ride creator"""
        return request.user == obj.offered_by


class IsNotRideOwner(BasePermission):
    """Verify requesting user is NOT the ride owner"""

    def has_object_permission(self, request, view, obj):
        """Verify request user is NOT the ride creator"""
        return not request.user == obj.offered_by

