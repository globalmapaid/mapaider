from django.urls import path, include
from .views import SignInAPIView, CurrentUserAPIView
from dj_rest_auth.views import LogoutView

urlpatterns = [
    path('user', CurrentUserAPIView.as_view(), name='rest_user_details'),
    path('login', SignInAPIView.as_view(), name='rest_login'),
    path('logout', LogoutView.as_view(), name='rest_logout'),
    path('register/', include('dj_rest_auth.registration.urls')),
]
