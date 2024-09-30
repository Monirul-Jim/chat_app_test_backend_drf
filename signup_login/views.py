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


class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializers(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)

                login(request, user)

                response = Response({
                    'message': 'User logged in successfully',
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email
                }, status=status.HTTP_200_OK)

                response.set_cookie(
                    'refresh', str(refresh),
                    httponly=True,
                    # secure=False,
                    # samesite='None',
                    # samesite=None,
                )
                return response
            else:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


def add_user(request):
    if request.method == 'POST':
        serializer = AddedUserSerializer(data=request.data)
        if serializer.is_valid():
            # Set the added_by field to the current user
            serializer.save(added_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_added_users(request):
    added_users = AddedUser.objects.all()
    serializer = AddedUserSerializer(added_users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
