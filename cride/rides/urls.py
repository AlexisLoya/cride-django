"""Rides urls."""
# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import rides as rides_view
route = DefaultRouter()
route.register(r'circles/(?P<slug_name>[-a-zA-Z0-0_]+)/rides', rides_view.RideViewSet, basename='ride')
urlpatterns = [
    path('', include(route.urls))
]
