from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.managers import ActiveManager


class Orderable(models.Model):
    """
    An abstract class for models that are orderable.
    """

    order = models.IntegerField(
        default=0,
        verbose_name=_('order'),
    )

    class Meta:
        abstract = True
        ordering = ['order']


class ActiveMixin(models.Model):
    """
    An abstract base class model that can be active or not
    """

    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    active_objects = ActiveManager()

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    """
    An abstract base class model with creation and modification date and time
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SocialMediaMixin(models.Model):
    """
    An abstract base class model with social media links
    """

    facebook_link = models.URLField(
        null=True,
        blank=True,
        verbose_name=_('facebook page'),
    )
    youtube_link = models.URLField(
        null=True,
        blank=True,
        verbose_name=_('youtube page'),
    )
    instagram_link = models.URLField(
        null=True,
        blank=True,
        verbose_name=_('instagram page'),
    )
    x_link = models.URLField(
        null=True,
        blank=True,
        verbose_name=_('x page'),
    )
    tiktok_link = models.URLField(
        null=True,
        blank=True,
        verbose_name=_('tiktok page'),
    )

    class Meta:
        abstract = True
