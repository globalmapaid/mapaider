import pytest


@pytest.mark.django_db
class TestShowMap:
    base_url = '/mapaider/map/'

    def test_returns_200_for_valid_slug_format(self, client):
        response = client.get(self.base_url + 'any-slug')
        assert response.status_code == 200

    def test_returns_200_for_nonexistent_slug(self, client):
        # View passes slug straight to the template; no DB lookup is performed.
        response = client.get(self.base_url + 'nonexistent-slug')
        assert response.status_code == 200

    def test_response_content_type_is_html(self, client):
        response = client.get(self.base_url + 'test-slug')
        assert 'text/html' in response['Content-Type']

    def test_template_used_is_map_viewer(self, client):
        response = client.get(self.base_url + 'test-slug')
        template_names = [t.name for t in response.templates]
        assert 'mapaider/map-viewer.html' in template_names

    def test_slug_is_in_template_context(self, client):
        response = client.get(self.base_url + 'my-map')
        assert response.context['slug'] == 'my-map'

    def test_html_contains_map_div(self, client):
        response = client.get(self.base_url + 'test-slug')
        assert b'<div id="map">' in response.content

    def test_xframe_options_header_absent(self, client):
        response = client.get(self.base_url + 'test-slug')
        assert response.get('X-Frame-Options') is None
