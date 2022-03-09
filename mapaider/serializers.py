from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Map, Layer, MapFeature


class MapFeatureSerializer(GeoFeatureModelSerializer):
    feature_data = serializers.SerializerMethodField()

    class Meta:
        model = MapFeature
        geo_field = 'geom'
        fields = ['uuid', 'name', 'feature_data']

    @staticmethod
    def get_feature_data(obj):
        return obj.data


class LayerSerializer(serializers.ModelSerializer):
    features = MapFeatureSerializer(many=True)

    class Meta:
        model = Layer
        fields = ['uuid', 'name', 'features']


class MapSerializer(serializers.ModelSerializer):
    layers = LayerSerializer(many=True)

    class Meta:
        model = Map
        # layers = LayerSerializer(many=True)
        fields = ['uuid', 'slug', 'name', 'layers']
        # depth = 1
