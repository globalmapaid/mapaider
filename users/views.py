from dj_rest_auth.views import LogoutView as DjRestAuthLogoutView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer, LoginSerializer


class LogoutView(DjRestAuthLogoutView):
    permission_classes = [permissions.IsAuthenticated]


class SignInAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        (token, _) = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })


class CurrentUserAPIView(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
