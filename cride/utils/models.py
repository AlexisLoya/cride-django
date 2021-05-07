"""Django model utilities"""

# Django
from django.db import models

class CRideModel(models.Model):
    """inherit from ride base model.
    CRideModel acts as an abstract base class from which every
    other model in the project eill inherit. This class provides
    every table with the following atributes:
        - created (Datetime): Store the datatime the object was created
        - modified (Datetime): Store the datatime the object was modified
    """
    created = models.DateTimeField(
        'created at',
        auto_now_add = True,
        help_text='Date time in which the object was created'
    )
    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time in which the object was modified'
    )
class Meta:
    """Meta options"""
    abstract = True
    get_lastest_by = 'created'
    ordering = ['-created', '-modified']
