import uuid
from django.db import models
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
    created_at = models.DateTimeField(_('Date Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Date Updated'), auto_now=True)

    maps = models.ManyToManyField('Map', through='MapLayer')

    class Meta:
        verbose_name = 'Layer'
        verbose_name_plural = 'Layers'

    def __str__(self):
        return self.name


class MapLayer(models.Model):
    map = models.ForeignKey('Map', on_delete=models.CASCADE)
    layer = models.ForeignKey('Layer', on_delete=models.CASCADE)
    label = models.CharField(
        _('layer title'),
        max_length=80, blank=True, null=True,
        help_text='Leave blank to inherit the layer name'    )
    priority = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = [['map', 'layer']]

    def __str__(self):
        return f'{self.map.name} - {self.layer.name}'

