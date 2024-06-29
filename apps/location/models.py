from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel


class Region(TimeStampedModel):
    name = models.CharField(max_length=120, verbose_name=_("Name"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is activate"))

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def __str__(self):
        return f"{self.name}"


class Area(TimeStampedModel):
    name = models.CharField(max_length=120, verbose_name=_("Name"))
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='region', verbose_name=_("Region"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is activate"))

    # objects = BaseManager()

    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")

    def __str__(self):
        return f"{self.name}"


class Village(TimeStampedModel):
    name = models.CharField(max_length=120, verbose_name=_("Name"))
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='area', verbose_name=_("Area"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is activate"))

    # objects = BaseManager()

    class Meta:
        verbose_name = _("Village")
        verbose_name_plural = _("Villages")

    def __str__(self):
        return f"{self.name}"
