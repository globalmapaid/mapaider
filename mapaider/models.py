import uuid
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, Polygon
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Organization(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('organisation name'), max_length=80)
    slug = models.SlugField(_('slug'), max_length=80, unique=True, blank=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this project should be treated as active. '
            'Unselect this instead of deleting projects.'
        ),
    )
    created_at = models.DateTimeField(_('Date Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Date Updated'), auto_now=True)

    class Meta:
        verbose_name = 'Organisation'
        verbose_name_plural = 'Organisations'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Map(models.Model):
    uuid = models.UUIDField(_('uuid'), db_index=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    name = models.CharField(_('map name'), max_length=80)
    slug = models.SlugField(_('slug'), max_length=80, blank=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this map should be treated as active. '
            'Unselect this instead of deleting maps.'
        ),
    )
    created_at = models.DateTimeField(_('Date Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Date Updated'), auto_now=True)

    layers = models.ManyToManyField('Layer', through='MapLayer')

    class Meta:
        verbose_name = 'Map'
        verbose_name_plural = 'Maps'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Layer(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    name = models.CharField(_('layer name'), max_length=80)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this layer should be treated as active. '
            'Unselect this instead of deleting layers.'
        ),
    )
    contribution = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('Date Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Date Updated'), auto_now=True)

    class Meta:
        verbose_name = 'Layer'
        verbose_name_plural = 'Layers'

    def __str__(self):
        return self.name


class MapLayer(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
    map = models.ForeignKey('Map', on_delete=models.CASCADE)
    layer = models.ForeignKey('Layer', on_delete=models.CASCADE)
    label = models.CharField(
        _('layer title'),
        max_length=80, blank=True, null=True,
        help_text='Leave blank to inherit the layer name')
    priority = models.PositiveSmallIntegerField(default=1)
    contribution = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('Date Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Date Updated'), auto_now=True)

    class Meta:
        unique_together = [['map', 'layer']]
        ordering = ['priority',]

    def __str__(self):
        return f'{self.map.name} - {self.layer.name}'


class MapFeature(models.Model):
    VIS_NONE = 0
    VIS_RESTRICTED = 2
    VIS_DEFAULT = 4

    VISIBILITY_OPTIONS = [
        (VIS_NONE, 'None'),
        (VIS_RESTRICTED, 'Restricted'),
        (VIS_DEFAULT, 'Default'),
    ]

    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
    layer = models.ForeignKey('Layer', related_name='features', on_delete=models.CASCADE)
    name = models.CharField(_('feature name'), max_length=80)
    geom = models.GeometryField(_('geometry'), srid=4326, null=True, geography=True)
    geom_type = models.CharField(_('geometry type'), max_length=16, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    data = models.JSONField(_('feature data'), null=True, blank=True, default=dict)
    visibility = models.IntegerField(_('visibility'), choices=VISIBILITY_OPTIONS, default=VIS_NONE)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)

    class Meta:
        verbose_name = 'Map Feature'
        verbose_name_plural = 'Map Features'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.geom is not None:
            self.geom_type = self.geom.geom_type

            centroid: Point
            if self.geom.geom_type == 'Polygon':
                self.geom: Polygon
                geom = self.geom.transform(27700, clone=True)
            elif self.geom.geom_type == 'Point':
                self.geom: Point
                geom = self.geom
            else:
                geom = self.geom

            centroid = geom.centroid

            (self.longitude, self.latitude) = centroid.coords
        else:
            self.longitude = None
            self.latitude = None
        return super().save(*args, **kwargs)
