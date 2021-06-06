import uuid as uuid
from django.contrib.gis.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

MEASUREMENT_UNITS = [
    ('m2', 'm2'),
    ('acres', 'Acres'),
    ('ha', 'Hectares'),
]


class PledgeType(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        verbose_name = 'Pledge Type'
        verbose_name_plural = 'Pledge Types'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Pledge(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.ForeignKey('PledgeType', on_delete=models.RESTRICT)
    geom = models.GeometryField(srid=4326, null=True, geography=True)
    geom_type = models.CharField(max_length=16, null=True,blank=True)
    area = models.DecimalField(max_digits=16, decimal_places=6, default=0)
    measurement_unit = models.CharField(max_length=6, choices=MEASUREMENT_UNITS, default='ha')

    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    notes = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(_('Date Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Date Updated'), auto_now=True)

    class Meta:
        verbose_name = 'Pledge'
        verbose_name_plural = 'Pledges'

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.geom is not None:

            self.geom_type = self.geom.geom_type

            if self.geom.geom_type == 'Polygon':
                geom = self.geom.transform(27700, clone=True)
                self.area = geom.area / 10000
                self.measurement_unit = 'ha'
            return super().save(*args, **kwargs)






