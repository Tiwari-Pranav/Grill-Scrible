from accounts.views import *
from django.urls import path

urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('login/',LoginAPIView.as_view(),name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('refresh/', CustomTokenRefreshAPIView.as_view(), name='token_refresh'),
    path('profile/', CurrentUserView.as_view(), name='profile_detail'),
]
