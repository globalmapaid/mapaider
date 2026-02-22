from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from mapaider.models import Layer, Map, MapFeature, MapLayer, Organization


class Command(BaseCommand):
    help = 'Seed minimal data required for CI tests (idempotent)'

    def handle(self, *args, **options):
        org, created = Organization.objects.get_or_create(
            slug='ci-test-organization',
            defaults={'name': 'CI Test Organization'},
        )
        if created:
            self.stdout.write('Created organization: CI Test Organization')
        else:
            self.stdout.write('Organization already exists: CI Test Organization')

        map_obj, created = Map.objects.get_or_create(
            slug='ci-test-map',
            defaults={
                'organization': org,
                'name': 'CI Test Map',
                'is_active': True,
            },
        )
        if created:
            self.stdout.write('Created map: ci-test-map')
        else:
            self.stdout.write('Map already exists: ci-test-map')

        layer, created = Layer.objects.get_or_create(
            name='CI Test Layer',
            organization=org,
            defaults={'config': Layer.get_default_config()},
        )
        if created:
            self.stdout.write('Created layer: CI Test Layer')
        else:
            self.stdout.write('Layer already exists: CI Test Layer')

        _map_layer, created = MapLayer.objects.get_or_create(
            map=map_obj,
            layer=layer,
        )
        if created:
            self.stdout.write('Created map-layer link')
        else:
            self.stdout.write('Map-layer link already exists')

        point = Point(0.0, 51.5)  # Greenwich (lon, lat)
        _feature, created = MapFeature.objects.get_or_create(
            layer=layer,
            name='CI Test Feature',
            defaults={
                'geom': point,
                'visibility': MapFeature.VIS_DEFAULT,
            },
        )
        if created:
            self.stdout.write('Created map feature: CI Test Feature')
        else:
            self.stdout.write('Map feature already exists: CI Test Feature')

        self.stdout.write(self.style.SUCCESS('CI seed data ready.'))
