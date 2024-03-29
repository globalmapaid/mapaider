from django.contrib.auth import authenticate
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer as DRARegisterSerializer

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'email', 'first_name', 'last_name']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user

        raise serializers.ValidationError('Incorrect Credentials')


class RegisterSerializer(DRARegisterSerializer):
    username = None
