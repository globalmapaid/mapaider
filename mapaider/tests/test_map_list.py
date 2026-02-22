import pytest
from mapaider.tests.conftest import MapFactory


@pytest.mark.django_db
class TestMapList:
    url = '/api/mapaider/map'

    def test_returns_200_for_unauthenticated_request(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == 200

    def test_returns_empty_list_when_no_maps_exist(self, db, api_client):
        response = api_client.get(self.url)
        assert response.json() == []

    def test_returns_only_active_maps(self, api_client, organization):
        active_map = MapFactory(organization=organization, is_active=True)
        inactive_map = MapFactory(organization=organization, is_active=False)
        response = api_client.get(self.url)
        slugs = [m['slug'] for m in response.json()]
        assert active_map.slug in slugs
        assert inactive_map.slug not in slugs

    def test_response_shape_contains_uuid_name_slug(self, api_client, organization):
        MapFactory(organization=organization)
        response = api_client.get(self.url)
        data = response.json()
        assert len(data) == 1
        assert 'uuid' in data[0]
        assert 'name' in data[0]
        assert 'slug' in data[0]

    def test_returns_multiple_active_maps(self, api_client, organization):
        MapFactory.create_batch(3, organization=organization, is_active=True)
        response = api_client.get(self.url)
        assert len(response.json()) == 3
