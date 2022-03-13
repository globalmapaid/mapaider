from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeoFeatureModelListSerializer
from .models import MapProject, Layer, MapLayer, MapFeature


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
    # uuid = serializers.SerializerMethodField()
    # name = serializers.SerializerMethodField()
    # feature_set = serializers.SerializerMethodField()
    layer = LayerSerializer()

    class Meta:
        model = MapLayer
        fields = ['uuid', 'label', 'priority', 'contribution', 'layer']

    # @staticmethod
    # def get_uuid(obj):
    #     return obj.layer.uuid
    #
    # @staticmethod
    # def get_name(obj):
    #     return obj.layer.name
    #
    # @staticmethod
    # def get_feature_set(obj):
    #     return MapFeatureSerializer(obj.layer.features, many=True).data


class MapSerializer(serializers.ModelSerializer):
    layer_set = MapLayerSerializer(source='maplayer_set', many=True)

    class Meta:
        model = MapProject
        fields = ['uuid', 'slug', 'name', 'layer_set']
