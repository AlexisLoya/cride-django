"""Circles urls."""
# Django
from django.urls import path

# Views
from cride.circles.views import list_circles, create_circles

urlpatterns = [
    path('circles/',list_circles),
    path('circles/create',create_circles),
               ]
