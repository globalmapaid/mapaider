import pytest
from mapaider.tests.conftest import MapFactory


@pytest.mark.django_db
class TestMapDetail:
    base_url = '/api/mapaider/map/'

    def test_returns_200_for_valid_slug(self, api_client, map_layer):
        response = api_client.get(self.base_url + map_layer.map.slug)
        assert response.status_code == 200

    def test_returns_404_for_nonexistent_slug(self, db, api_client):
        response = api_client.get(self.base_url + 'does-not-exist')
        assert response.status_code == 404

    def test_response_contains_uuid_slug_name_links_layer_set(self, api_client, map_layer):
        response = api_client.get(self.base_url + map_layer.map.slug)
        data = response.json()
        for key in ['uuid', 'slug', 'name', 'links', 'layer_set']:
            assert key in data

    def test_layer_set_is_empty_when_no_layers_attached(self, api_client, organization):
        m = MapFactory(organization=organization)
        response = api_client.get(self.base_url + m.slug)
        assert response.json()['layer_set'] == []

    def test_layer_set_contains_attached_layers(self, api_client, map_layer):
        response = api_client.get(self.base_url + map_layer.map.slug)
        assert len(response.json()['layer_set']) == 1

    def test_visible_feature_appears_in_feature_set(self, api_client, map_layer, visible_feature):
        response = api_client.get(self.base_url + map_layer.map.slug)
        layer_data = response.json()['layer_set'][0]['layer']
        uuids = [f['properties']['uuid'] for f in layer_data['feature_set']['features']]
        assert str(visible_feature.uuid) in uuids

    def test_invisible_feature_excluded_from_feature_set(self, api_client, map_layer, invisible_feature):
        response = api_client.get(self.base_url + map_layer.map.slug)
        layer_data = response.json()['layer_set'][0]['layer']
        uuids = [f['properties']['uuid'] for f in layer_data['feature_set']['features']]
        assert str(invisible_feature.uuid) not in uuids

    def test_feature_set_is_geojson_featurecollection(self, api_client, map_layer, visible_feature):
        response = api_client.get(self.base_url + map_layer.map.slug)
        layer_data = response.json()['layer_set'][0]['layer']
        assert layer_data['feature_set']['type'] == 'FeatureCollection'
