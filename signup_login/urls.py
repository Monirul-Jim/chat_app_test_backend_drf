from django.urls import path
from .views import (add_user, get_added_users, get_registered_and_logged_in_users,
                    UserLoginApiView, UserRegistrationView)
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', UserLoginApiView.as_view(), name='user_login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logged-in-users/', get_registered_and_logged_in_users,
         name='logged_in_users'),
    path('add-user/', add_user, name='add_user'),
    path('get-added-users/', get_added_users, name='get_added_users'),
]
