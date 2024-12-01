from django.urls import path

from .views import AuthUserView, ProfileView, LoginView

urlpatterns = [
    path('auth/', AuthUserView.as_view(), name='authentication'),
    path('login/', LoginView.as_view(), name='authorization'),
    path('profile/<str:pass_code>', ProfileView.as_view(), name='profile'),
]