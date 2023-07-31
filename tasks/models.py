from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _

# Create your models here.

class ListModel(BaseModel):
    title = models.CharField(verbose_name=_("Title"),max_length=100,
                            help_text=_("Enter List title"))
    board = models.ForeignKey('Board', on_delete=models.CASCADE, related_name='lists')
    
    COLOR_CHOICES = [
        ('red',    'Red'),
        ('blue',   'Blue'),
        ('green',  'Green'),
        ('orange', 'Orange'),
        ('purple', 'Purple'),
        ('yellow', 'Yellow'),
    ]
    background_color = models.CharField(
        max_length=10,choices=COLOR_CHOICES, null=True, blank=True)
    
    
    
    