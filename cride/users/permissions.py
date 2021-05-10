"""User permissions"""

# Django Rest Framework
from rest_framework.permissions import BasePermission

class IsAccountOwner(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_object_permission(self, request, view, obj):
        """Check obk and user are the same"""
        return request.user == obj