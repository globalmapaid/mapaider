from rest_framework import serializers

from mapaider.models import MapLayer


class MapLayerContributionAccess:
    def __call__(self, uuid):
        try:
            maplayer: MapLayer = MapLayer.objects.get(uuid=uuid)

            if not (maplayer.contribution and maplayer.layer.contribution):
                raise serializers.ValidationError('Layer is not open to contribution')
        except MapLayer.DoesNotExist:
            raise serializers.ValidationError('Layer not found')
