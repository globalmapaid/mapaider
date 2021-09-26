from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Pledge


class PledgeSerializer(GeoFeatureModelSerializer):
    postcode = serializers.SerializerMethodField()

    class Meta:
        model = Pledge
        geo_field = 'geom'
        fields = ['uuid', 'geom', 'area', 'measurement_unit', 'first_name', 'last_name', 'email', 'phone', 'street',
                  'city', 'postcode', 'postcode', 'type', 'notes', 'reason']
        read_only_fields = ['uuid', 'created_at', 'updated_at', 'submitted_at', 'visibility']

    def get_postcode(self, instance):
        if instance.visibility == 2:
            return 'Restricted Postcode'
        else:
            return instance.postcode


class PledgeCreateSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Pledge
        geo_field = 'geom'
        fields = ['uuid', 'geom', 'area', 'measurement_unit', 'first_name', 'last_name', 'email', 'phone', 'street',
                  'city', 'postcode', 'type', 'notes', 'reason']
        read_only_fields = ['uuid', 'created_at', 'updated_at', 'submitted_at', 'visibility']        