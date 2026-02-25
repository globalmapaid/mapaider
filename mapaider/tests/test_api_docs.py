import pytest


@pytest.mark.django_db
class TestApiDocs:
    def test_swagger_ui_returns_200(self, api_client):
        response = api_client.get('/api/doc/')
        assert response.status_code == 200

    def test_swagger_ui_content_type_is_html(self, api_client):
        response = api_client.get('/api/doc/')
        assert 'text/html' in response['Content-Type']

    def test_schema_endpoint_returns_200(self, api_client):
        response = api_client.get('/api/doc/schema/')
        assert response.status_code == 200

    def test_schema_endpoint_content_type_is_yaml(self, api_client):
        response = api_client.get('/api/doc/schema/')
        assert 'application/vnd.oai.openapi' in response['Content-Type']

    def test_schema_endpoint_returns_json_when_requested(self, api_client):
        response = api_client.get('/api/doc/schema/?format=json')
        assert response.status_code == 200
        assert 'application/vnd.oai.openapi+json' in response['Content-Type']