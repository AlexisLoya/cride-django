"""Circle views"""

# Django Rest Frameworks
from rest_framework import viewsets, mixins

# Serializers
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions import IsCircleAdmin
from cride.circles.serializers.circle import CircleModelSerializer

# Model
from cride.circles.models import Circle, Membership

class CircleViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Circle view set"""
    #queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Restrict list to public-only"""
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset

    def get_permissions(self):
        """Assign permissions based on actions"""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [p() for p in permissions]


    def perform_create(self, serializer):
        """Assign circle admin."""
        circle = serializer.save()
        user  = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remainig_invitations=10
        )
