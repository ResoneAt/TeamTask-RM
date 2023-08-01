from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name=_('created at'),
                                      auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(verbose_name=_('Is Deleted'),
                                     default=False)
    deleted_at = models.DateTimeField(verbose_name=_('Deleted at'),
                                      null=True,
                                      blank=True,
                                      editable=False)

    class Meta:
        abstract = True
