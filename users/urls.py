from django.urls import path, include
from .views import SignInAPI, CurrentUser
from knox import views as knox_views


# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    path(r'auth/', include('knox.urls')),
    path('auth/login', SignInAPI.as_view()),
    path('auth/user/', CurrentUser.as_view()),
]
