"""Circles urls."""
# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import circles as circle_view
from .views import memberships as membership_views

route = DefaultRouter()
route.register(r'circles', circle_view.CircleViewSet, basename='circle')
route.register(r'circles/(?P<slug_name>[a-zA-Z0-9_-]+)/members',
               membership_views.MembershipViewSet, base_name='membership')
urlpatterns = [
    path('', include(route.urls))
]
