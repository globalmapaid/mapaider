import uuid as uuid
from datetime import datetime

from django.contrib.gis.geos import Point, Polygon
from pytz import timezone
from django.contrib.gis.db import models
from django.db import connection
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
    VIS_NONE = 0
    VIS_RESTRICTED = 2
    VIS_DEFAULT = 4

    VISIBILITY_OPTIONS = [
        (VIS_NONE, 'None'),
        (VIS_RESTRICTED, 'Restricted'),
        (VIS_DEFAULT, 'Default'),
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.ForeignKey('PledgeType', on_delete=models.RESTRICT)
    geom = models.GeometryField(srid=4326, null=True, geography=True)
    geom_type = models.CharField(max_length=16, null=True, blank=True)
    area = models.DecimalField(max_digits=16, decimal_places=6, default=0)
    measurement_unit = models.CharField(max_length=6, choices=MEASUREMENT_UNITS, default='ha')
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=12, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    reason = models.CharField(max_length=255, null=True, blank=True)
    visibility = models.IntegerField(_('Visibility'), choices=VISIBILITY_OPTIONS, default=VIS_NONE)
    submitted_at = models.DateTimeField(_('Date Submitted'), null=True, blank=True)
    created_at = models.DateTimeField(_('Date Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Date Updated'), auto_now=True)

    class Meta:
        verbose_name = 'Pledge'
        verbose_name_plural = 'Pledges'

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {} CASCADE'.format(cls._meta.db_table))

    @property
    def name(self):
        first_name = self.first_name if self.first_name is not None else ''
        last_name = self.last_name if self.last_name is not None else ''
        name = ' '.join([first_name, last_name]).strip()

        return name if name != '' else '<Unnamed>'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.geom is not None:

            self.geom_type = self.geom.geom_type
            if self.submitted_at is None:
                self.submitted_at = datetime.now(tz=timezone('UTC'))

            centroid: Point
            if self.geom.geom_type == 'Polygon':
                self.geom: Polygon
                geom = self.geom.transform(27700, clone=True)
                self.area = geom.area / 10000
                self.measurement_unit = 'ha'

                centroid = self.geom.centroid
            elif self.geom.geom_type == 'Point':
                self.geom: Point
                centroid = self.geom.centroid
            (self.longitude, self.latitude) = centroid.coords
        else:
            self.longitude = None
            self.latitude = None
        return super().save(*args, **kwargs)
