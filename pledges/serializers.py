from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Pledge


class PledgeSerializer(GeoFeatureModelSerializer):

    postcode = serializers.SerializerMethodField()

    class Meta:
        model = Pledge
        geo_field = 'geom'
        fields = ['uuid', 'type', 'geom', 'area', 'measurement_unit', 'first_name',
                  'last_name', 'email', 'phone', 'street', 'city','postcode', 'notes', 'visibility']
        read_only_fields = ['uuid', 'created_at', 'updated_at']

    def get_postcode(self, instance):
        if instance.visibility == 2:
            return 'Restricted Postcode'
        else:
            return instance.postcode