from django.db import models

from queryset import CustomQuerysetMixin
            
class CustomQuerysetManager(CustomQuerysetMixin, models.Manager):
    pass
