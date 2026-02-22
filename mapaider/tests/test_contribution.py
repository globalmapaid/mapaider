import pytest
from mapaider.models import MapFeature


CONTRIBUTION_URL = '/api/mapaider/contribution/mapfeature'
VALID_GEOMETRY = {'type': 'Point', 'coordinates': [0.0, 51.5]}


@pytest.mark.django_db
class TestContributionMapFeature:

    def _post(self, client, maplayer_uuid, name='Test Feature', geometry=None):
        payload = {
            'maplayer': str(maplayer_uuid),
            'name': name,
            'geometry': geometry or VALID_GEOMETRY,
        }
        return client.post(CONTRIBUTION_URL, data=payload, format='json')

    def test_creates_feature_when_both_gates_open(self, api_client, contribution_map_layer):
        response = self._post(api_client, contribution_map_layer.uuid)
        assert response.status_code == 201

    def test_response_is_geojson_feature(self, api_client, contribution_map_layer):
        response = self._post(api_client, contribution_map_layer.uuid)
        assert response.json()['type'] == 'Feature'

    def test_created_feature_has_vis_none(self, api_client, contribution_map_layer):
        response = self._post(api_client, contribution_map_layer.uuid)
        feature_uuid = response.json()['properties']['uuid']
        feature = MapFeature.objects.get(uuid=feature_uuid)
        assert feature.visibility == MapFeature.VIS_NONE

    def test_returns_400_when_maplayer_contribution_false(self, api_client, non_contribution_map_layer):
        response = self._post(api_client, non_contribution_map_layer.uuid)
        assert response.status_code == 400

    def test_returns_400_when_only_maplayer_gate_open(self, api_client, half_gate_map_layer):
        response = self._post(api_client, half_gate_map_layer.uuid)
        assert response.status_code == 400

    def test_returns_400_for_nonexistent_maplayer_uuid(self, db, api_client):
        response = self._post(api_client, '00000000-0000-0000-0000-000000000000')
        assert response.status_code == 400

    def test_returns_400_when_name_missing(self, api_client, contribution_map_layer):
        payload = {
            'maplayer': str(contribution_map_layer.uuid),
            'geometry': VALID_GEOMETRY,
        }
        response = api_client.post(CONTRIBUTION_URL, data=payload, format='json')
        assert response.status_code == 400

    def test_returns_400_when_geometry_missing(self, api_client, contribution_map_layer):
        payload = {
            'maplayer': str(contribution_map_layer.uuid),
            'name': 'Test Feature',
        }
        response = api_client.post(CONTRIBUTION_URL, data=payload, format='json')
        assert response.status_code == 400

    def test_returns_400_when_geometry_invalid(self, api_client, contribution_map_layer):
        response = self._post(
            api_client,
            contribution_map_layer.uuid,
            geometry='not-a-geojson',
        )
        assert response.status_code == 400
