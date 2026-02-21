import pytest
from mapaider.models import MapFeature


@pytest.mark.django_db
class TestLayerDetail:
    base_url = '/api/mapaider/layer/'

    def test_returns_200_for_valid_uuid(self, api_client, layer):
        response = api_client.get(self.base_url + str(layer.uuid))
        assert response.status_code == 200

    def test_returns_404_for_nonexistent_uuid(self, db, api_client):
        response = api_client.get(self.base_url + '00000000-0000-0000-0000-000000000000')
        assert response.status_code == 404

    def test_response_shape(self, api_client, layer):
        response = api_client.get(self.base_url + str(layer.uuid))
        data = response.json()
        for key in ['uuid', 'name', 'config', 'field_set', 'feature_set']:
            assert key in data

    def test_config_merges_defaults(self, api_client, layer):
        response = api_client.get(self.base_url + str(layer.uuid))
        config = response.json()['config']
        assert 'clustering' in config

    def test_visible_feature_included(self, api_client, layer, visible_feature):
        response = api_client.get(self.base_url + str(layer.uuid))
        uuids = [
            f['properties']['uuid']
            for f in response.json()['feature_set']['features']
        ]
        assert str(visible_feature.uuid) in uuids

    def test_invisible_feature_excluded(self, api_client, layer, invisible_feature):
        response = api_client.get(self.base_url + str(layer.uuid))
        uuids = [
            f['properties']['uuid']
            for f in response.json()['feature_set']['features']
        ]
        assert str(invisible_feature.uuid) not in uuids
