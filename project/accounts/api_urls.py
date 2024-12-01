from django.urls import path

from .views import api_profile, api_activate_code, api_login, api_auth

urlpatterns = [
    path('auth/', api_auth, name='api_authentication'),
    path('login/', api_login, name='api_authorization'),
    path('activate/', api_activate_code, name='api_activate_code'),
    path('profile/', api_profile, name='api_profile'),
]
