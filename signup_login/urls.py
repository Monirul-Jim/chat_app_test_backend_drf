from django.urls import path
from .views import (AddUserView, AddedUserListView, get_registered_and_logged_in_users,
                    UserLoginApiView, UserRegistrationView, UserLogoutApiView)
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', UserLoginApiView.as_view(), name='user_login'),
    path('logout/', UserLogoutApiView.as_view(), name='user_logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logged-in-users/', get_registered_and_logged_in_users,
         name='logged_in_users'),
    path('add-user/', AddUserView.as_view(), name='add_user'),
    path('get-added-users/', AddedUserListView.as_view(), name='get_added_users'),
]
