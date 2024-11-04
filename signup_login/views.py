from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from signup_login.models import AddedUser
from .serializers import AddedUserSerializer, UserLoginSerializers, UserRegistrationSerializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import JsonResponse
from django.db import models
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.middleware.csrf import get_token


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None


# class UserLoginApiView(APIView):
#     def post(self, request):
#         serializer = UserLoginSerializers(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']
#             user = authenticate(request, email=email, password=password)
#             if user is not None:
#                 refresh = RefreshToken.for_user(user)
#                 response = Response({
#                     'message': 'User logged in successfully',
#                     'access': str(refresh.access_token),
#                     'user_id': user.id,
#                     'username': user.username,
#                     'email': user.email
#                 }, status=status.HTTP_200_OK)

#                 response.set_cookie(
#                     key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
#                     value=str(refresh),
#                     expires=timedelta(days=30),
#                     httponly=True,
#                     secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
#                     samesite='Lax'
#                 )
#                 return response
#             else:
#                 return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializers(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)

                response = Response({
                    'message': 'User logged in successfully',
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email
                }, status=status.HTTP_200_OK)

                # Set the refresh token cookie
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                    value=str(refresh),
                    expires=timedelta(days=30),
                    httponly=True,
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    samesite='Lax'
                )

                # Set the CSRF token cookie
                csrf_token = get_token(request)
                response.set_cookie(
                    key="csrftoken",
                    value=csrf_token,
                    httponly=False,  # Allows JavaScript to read it for front-end requests
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    samesite='Lax'
                )

                return response
            else:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        response = Response(
            {'message': 'User logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie('refresh')
        return response


# this is just for login user show

# def get_logged_in_users(request):
#     sessions = Session.objects.filter(expire_date__gte=timezone.now())
#     user_id_list = []
#     for session in sessions:
#         data = session.get_decoded()
#         user_id = data.get('_auth_user_id')
#         if user_id:
#             user_id_list.append(user_id)

#     logged_in_users = User.objects.filter(
#         id__in=user_id_list, is_superuser=False)
#     user_data = [{'id': user.id, 'username': user.username,
#                   'email': user.email} for user in logged_in_users]

#     return JsonResponse(user_data, safe=False)


# def get_registered_and_logged_in_users(request):
#     users = User.objects.filter(
#         last_login__isnull=False).exclude(is_superuser=True)
#     users_data = [
#         {
#             'username': user.username,
#             'email': user.email,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#         }
#         for user in users
#     ]
#     return JsonResponse(users_data, safe=False)

def get_registered_and_logged_in_users(request):
    search_query = request.GET.get('search', '')
    users = User.objects.filter(
        last_login__isnull=False).exclude(is_superuser=True)

    if search_query:
        search_terms = search_query.split()

        if len(search_terms) == 1:
            users = users.filter(
                models.Q(username__icontains=search_query) |
                models.Q(email__icontains=search_query) |
                models.Q(first_name__icontains=search_query) |
                models.Q(last_name__icontains=search_query)
            )
        elif len(search_terms) >= 2:
            users = users.filter(
                models.Q(first_name__icontains=search_terms[0]) &
                models.Q(last_name__icontains=search_terms[1])
            )

    users_data = [
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        for user in users
    ]

    return JsonResponse(users_data, safe=False)


# class AddUserView(APIView):
#     def post(self, request):
#         data = request.data
#         added_by_id = data.get('added_by')
#         try:
#             added_by_user = User.objects.get(id=added_by_id)
#         except User.DoesNotExist:
#             return Response({'error': 'Invalid added_by user ID'}, status=status.HTTP_400_BAD_REQUEST)
#         serializer = AddedUserSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save(added_by=added_by_user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddUserView(APIView):
    def post(self, request):
        data = request.data
        added_by_id = data.get('added_by')

        # Find the user who is adding the new user
        try:
            added_by_user = User.objects.get(id=added_by_id)
        except User.DoesNotExist:
            return Response({'error': 'Invalid added_by user ID'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the same added_by user has already added this email or username
        email = data.get('email')
        username = data.get('username')

        if AddedUser.objects.filter(email=email, added_by=added_by_user).exists() or AddedUser.objects.filter(username=username, added_by=added_by_user).exists():
            return Response({'error': 'You have already added this user.'}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with adding the user if the user is not already added by the same added_by user
        serializer = AddedUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save(added_by=added_by_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddedUserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            added_users = AddedUser.objects.filter(added_by=request.user)
            serializer = AddedUserSerializer(added_users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Authentication required.'}, status=status.HTTP_403_FORBIDDEN)
