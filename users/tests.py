import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from mapaider.tests.conftest import UserFactory


# ── Existing manager tests (kept intact) ──────────────────────────────────────

class AuthManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)


# ── Auth API tests ─────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestSignInAPIView:
    url = '/api/auth/login'

    def test_returns_token_on_valid_credentials(self, db):
        user = UserFactory()
        client = APIClient()
        response = client.post(self.url, {'email': user.email, 'password': 'testpass123'})
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        assert 'user' in data

    def test_user_object_contains_uuid_email(self, db):
        user = UserFactory()
        client = APIClient()
        response = client.post(self.url, {'email': user.email, 'password': 'testpass123'})
        user_data = response.json()['user']
        assert 'uuid' in user_data
        assert 'email' in user_data
        assert user_data['email'] == user.email

    def test_returns_400_on_wrong_password(self, db):
        user = UserFactory()
        client = APIClient()
        response = client.post(self.url, {'email': user.email, 'password': 'wrongpassword'})
        assert response.status_code == 400

    def test_returns_400_on_nonexistent_email(self, db):
        client = APIClient()
        response = client.post(self.url, {'email': 'nobody@example.com', 'password': 'any'})
        assert response.status_code == 400

    def test_returns_400_when_email_missing(self, db):
        client = APIClient()
        response = client.post(self.url, {'password': 'testpass123'})
        assert response.status_code == 400

    def test_returns_400_when_password_missing(self, db):
        user = UserFactory()
        client = APIClient()
        response = client.post(self.url, {'email': user.email})
        assert response.status_code == 400


@pytest.mark.django_db
class TestCurrentUserAPIView:
    url = '/api/auth/user'

    def _auth_client(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return client

    def test_returns_200_with_valid_token(self, db):
        user = UserFactory()
        response = self._auth_client(user).get(self.url)
        assert response.status_code == 200

    def test_returns_correct_user_data(self, db):
        user = UserFactory()
        response = self._auth_client(user).get(self.url)
        data = response.json()
        assert data['email'] == user.email
        assert str(data['uuid']) == str(user.uuid)

    def test_returns_401_without_token(self, db):
        response = APIClient().get(self.url)
        assert response.status_code == 401

    def test_returns_401_with_invalid_token(self, db):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token invalidtoken123')
        response = client.get(self.url)
        assert response.status_code == 401


@pytest.mark.django_db
class TestLogoutView:
    url = '/api/auth/logout'

    def _auth_client_with_token(self):
        user = UserFactory()
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return client, token, user

    def test_returns_200_with_valid_token(self, db):
        client, _, __ = self._auth_client_with_token()
        response = client.post(self.url)
        assert response.status_code == 200

    def test_returns_401_without_token(self, db):
        response = APIClient().post(self.url)
        assert response.status_code == 401

    def test_token_is_deleted_after_logout(self, db):
        client, token, user = self._auth_client_with_token()
        client.post(self.url)
        assert not Token.objects.filter(user=user).exists()


@pytest.mark.django_db
@override_settings(
    ACCOUNT_EMAIL_VERIFICATION='none',
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
)
class TestRegistrationView:
    url = '/api/auth/register/'

    def _valid_payload(self, email='new@example.com'):
        return {
            'email': email,
            'password1': 'Str0ng!Pass#99',
            'password2': 'Str0ng!Pass#99',
        }

    def test_returns_201_with_valid_data(self, db):
        response = APIClient().post(self.url, data=self._valid_payload())
        assert response.status_code == 201

    def test_user_is_created_in_db(self, db):
        User = get_user_model()
        APIClient().post(self.url, data=self._valid_payload(email='created@example.com'))
        assert User.objects.filter(email='created@example.com').exists()

    def test_returns_400_when_passwords_dont_match(self, db):
        payload = self._valid_payload()
        payload['password2'] = 'DifferentPass#99'
        response = APIClient().post(self.url, data=payload)
        assert response.status_code == 400

    def test_returns_400_when_email_already_exists(self, db):
        UserFactory(email='existing@example.com')
        response = APIClient().post(self.url, data=self._valid_payload(email='existing@example.com'))
        assert response.status_code == 400

    def test_returns_400_when_email_missing(self, db):
        payload = {'password1': 'Str0ng!Pass#99', 'password2': 'Str0ng!Pass#99'}
        response = APIClient().post(self.url, data=payload)
        assert response.status_code == 400
