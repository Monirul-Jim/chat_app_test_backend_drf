from django.urls import path
from .views import UserRegistrationView, UserLoginApiView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', UserLoginApiView.as_view(), name='user_login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
