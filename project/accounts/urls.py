from django.urls import path

from .views import AuthUserView, SuccessfulAuth, activate_code, ProfileView, LoginView

urlpatterns = [
    path('auth/', AuthUserView.as_view(), name='authentication'),
    path('login/', LoginView.as_view(), name='authorization'),
    path('activate/', activate_code, name='activate_code'),
    path('profile/<str:pass_code>', ProfileView.as_view(), name='profile'),
    path('successful_auth/', SuccessfulAuth.as_view(), name='successful_auth'),
]