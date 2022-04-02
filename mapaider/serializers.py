from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeoFeatureModelListSerializer
from .models import Map, Layer, MapLayer, MapFeature, MapLink
from .validators import MapLayerContributionAccess


class MapViewerVisibleFeatureSerializer(GeoFeatureModelListSerializer):
    def to_representation(self, data):
        data = data.filter(visibility__gt=0)
        return super(MapViewerVisibleFeatureSerializer, self).to_representation(data)

    def update(self, instance, validated_data):
        super()


class MapViewerMapFeatureSerializer(GeoFeatureModelSerializer):
    feature_data = serializers.SerializerMethodField()

    class Meta:
        model = MapFeature
        list_serializer_class = MapViewerVisibleFeatureSerializer
        geo_field = 'geom'
        fields = ['uuid', 'name', 'feature_data']

    @staticmethod
    def get_feature_data(obj):
        return obj.data


class MapViewerLayerSerializer(serializers.ModelSerializer):
    feature_set = serializers.SerializerMethodField()

    class Meta:
        model = Layer
        fields = ['uuid', 'name', 'field_set', 'feature_set']

    @staticmethod
    def get_feature_set(obj):
        return MapViewerMapFeatureSerializer(obj.features, many=True).data


class MapViewerMapLayerSerializer(serializers.ModelSerializer):
    layer = MapViewerLayerSerializer()

    class Meta:
        model = MapLayer
        fields = ['uuid', 'label', 'priority', 'contribution', 'layer']


class MapViewerMapLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapLink
        fields = ['uuid', 'label', 'url', 'sort']


class MapViewerMapSerializer(serializers.ModelSerializer):
    layer_set = MapViewerMapLayerSerializer(source='maplayer_set', many=True, read_only=True)
    links = MapViewerMapLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Map
        fields = ['uuid', 'slug', 'name', 'links', 'layer_set']


class ContributionMapFeatureSerializer(serializers.Serializer):
    maplayer = serializers.UUIDField(validators=[MapLayerContributionAccess()])
    name = serializers.CharField(max_length=80)
    geometry = gis_serializers.GeometryField()
    data = serializers.JSONField(default={})

    def create(self, validated_data: dict):
        map_layer: MapLayer = MapLayer.objects.get(uuid=validated_data.get('maplayer'))

        return MapFeature.objects.create(
            layer=map_layer.layer,
            name=validated_data.get('name'),
            geom=validated_data.get('geometry'),
            data=validated_data.get('data'),
            visibility=MapFeature.VIS_NONE
        )

    def update(self, instance, validated_data):
        pass
