import pytest
import factory
from django.contrib.gis.geos import Point
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from mapaider.models import Map, Layer, MapLayer, MapFeature, Organization
from users.models import User


# ── Factories ─────────────────────────────────────────────────────────────────

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    is_active = True
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Sequence(lambda n: f'Organization {n}')
    is_active = True


class LayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Layer

    organization = factory.SubFactory(OrganizationFactory)
    name = factory.Sequence(lambda n: f'Layer {n}')
    contribution = False


class MapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Map

    organization = factory.SubFactory(OrganizationFactory)
    name = factory.Sequence(lambda n: f'Map {n}')
    is_active = True


class MapLayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MapLayer

    map = factory.SubFactory(MapFactory)
    layer = factory.SubFactory(LayerFactory)
    contribution = False


class MapFeatureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MapFeature

    layer = factory.SubFactory(LayerFactory)
    name = factory.Sequence(lambda n: f'Feature {n}')
    geom = Point(0.0, 51.5)
    visibility = MapFeature.VIS_DEFAULT


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def auth_client(db):
    u = UserFactory()
    token, _ = Token.objects.get_or_create(user=u)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client


@pytest.fixture
def organization(db):
    return OrganizationFactory()


@pytest.fixture
def layer(db, organization):
    return LayerFactory(organization=organization)


@pytest.fixture
def map(db, organization):
    return MapFactory(organization=organization)


@pytest.fixture
def map_layer(db, map, layer):
    return MapLayerFactory(map=map, layer=layer)


@pytest.fixture
def visible_feature(db, layer):
    return MapFeatureFactory(layer=layer, visibility=MapFeature.VIS_DEFAULT)


@pytest.fixture
def invisible_feature(db, layer):
    return MapFeatureFactory(layer=layer, visibility=MapFeature.VIS_NONE)


@pytest.fixture
def contribution_map_layer(db, organization):
    """Both MapLayer.contribution=True and Layer.contribution=True — both gates open."""
    contrib_layer = LayerFactory(organization=organization, contribution=True)
    contrib_map = MapFactory(organization=organization)
    return MapLayerFactory(map=contrib_map, layer=contrib_layer, contribution=True)


@pytest.fixture
def non_contribution_map_layer(db, organization):
    """Both gates closed."""
    closed_layer = LayerFactory(organization=organization, contribution=False)
    closed_map = MapFactory(organization=organization)
    return MapLayerFactory(map=closed_map, layer=closed_layer, contribution=False)


@pytest.fixture
def half_gate_map_layer(db, organization):
    """MapLayer.contribution=True but Layer.contribution=False — still fails the double-gate."""
    half_layer = LayerFactory(organization=organization, contribution=False)
    half_map = MapFactory(organization=organization)
    return MapLayerFactory(map=half_map, layer=half_layer, contribution=True)
