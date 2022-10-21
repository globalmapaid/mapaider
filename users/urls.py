from django.urls import path
from .views import SignInAPIView, CurrentUserAPIView
from knox import views as knox_views

urlpatterns = [
    path('user', CurrentUserAPIView.as_view(), name='auth.user'),
    path('login', SignInAPIView.as_view(), name='auth.login'),
    path('logout', knox_views.LogoutView.as_view(), name='auth.logout'),
    path('logoutall', knox_views.LogoutAllView.as_view(), name='auth.logoutall'),
]
