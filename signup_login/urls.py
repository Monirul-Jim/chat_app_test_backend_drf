from django.urls import path
from .views import UserRegistrationView, UserLoginApiView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', UserLoginApiView.as_view(), name='user_login'),
]
