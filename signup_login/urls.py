from django.urls import path
from .views import UserRegistrationView, UserLoginApiView, get_registered_and_logged_in_users
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', UserLoginApiView.as_view(), name='user_login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logged-in-users/', get_registered_and_logged_in_users,
         name='logged_in_users'),
]
