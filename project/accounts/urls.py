from django.urls import path

from .views import auth, login, activate_code, profile

urlpatterns = [
    path("auth/", auth, name='authentication'),
    path("login/", login, name='authorization'),
    path("activate/", activate_code, name='activate_code'),
    path("profile/", profile, name='profile'),
]
