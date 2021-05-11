"""Circle memberships permission"""
from rest_framework.permissions import BasePermission

from cride.circles.models import Membership


class IsActiveCircleMember(BasePermission):
    """Allow access only to circle members.
    Expect thar the views implement this permission
    have a circle attribute assigned.
    """

    def has_permission(self, request, view):
        """Verify user is an active member of the circle"""
        try:
            Membership.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True

class IsSelfMember(BasePermission):
    """
    Allow accesses only to member owners
    """

    def has_permission(self, request, view):
        """Let object permission grant access"""
        membership = view.get_object()
        return self.has_object_permission(request, view, obj=membership)

    def has_object_permission(self, request, view, obj):
        """Allow access only if member is owned by the requesting user."""
        return request.user == obj.user
