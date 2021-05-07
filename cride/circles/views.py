"""Circles views"""

# Django
from django.http import HttpResponse


def list_circles(request):
    """list circles"""
    return HttpResponse('Hoal')
