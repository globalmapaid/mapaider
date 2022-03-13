from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeoFeatureModelListSerializer
from .models import Map, Layer, MapLayer, MapFeature, MapLink


class VisibleFeatureSerializer(GeoFeatureModelListSerializer):
    def to_representation(self, data):
        data = data.filter(visibility__gt=0)
        return super(VisibleFeatureSerializer, self).to_representation(data)


class MapFeatureSerializer(GeoFeatureModelSerializer):
    feature_data = serializers.SerializerMethodField()

    class Meta:
        model = MapFeature
        list_serializer_class = VisibleFeatureSerializer
        geo_field = 'geom'
        fields = ['uuid', 'name', 'feature_data']

    @staticmethod
    def get_feature_data(obj):
        return obj.data


class LayerSerializer(serializers.ModelSerializer):
    feature_set = serializers.SerializerMethodField()

    class Meta:
        model = Layer
        fields = ['uuid', 'name', 'feature_set']

    @staticmethod
    def get_feature_set(obj):
        return MapFeatureSerializer(obj.features, many=True).data


class MapLayerSerializer(serializers.ModelSerializer):
    layer = LayerSerializer()

    class Meta:
        model = MapLayer
        fields = ['uuid', 'label', 'priority', 'contribution', 'layer']


class MapLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapLink
        fields = ['uuid', 'label', 'url', 'sort']


class MapSerializer(serializers.ModelSerializer):
    layer_set = MapLayerSerializer(source='maplayer_set', many=True, read_only=True)
    links = MapLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Map
        fields = ['uuid', 'slug', 'name', 'links', 'layer_set']
