from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserLoginSerializers, UserRegistrationSerializers
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

# Create your views here.


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserLoginApiView(APIView):
#     def post(self, request):
#         serializer = UserLoginSerializers(data=self.request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']
#             user = authenticate(email=email, password=password)
#             if user:
#                 token, _ = Token.objects.get_or_create(user=user)
#                 login(request, user)
#                 return Response({
#                     'message': 'User logged in successfully',
#                     'token': token.key,
#                     'user_id': user.id
#                 }, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Invalid Credential'})

#         return Response(serializer.errors)
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
#             if user:
#                 token, _ = Token.objects.get_or_create(user=user)
#                 login(request, user)
#                 return Response({
#                     'message': 'User logged in successfully',
#                     'token': token.key,
#                     'user_id': user.id
#                 }, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserLoginApiView(APIView):
#     def post(self, request):
#         serializer = UserLoginSerializers(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']
#             user = authenticate(request, email=email, password=password)
#             if user:
#                 token, _ = Token.objects.get_or_create(user=user)
#                 login(request, user)
#                 return Response({
#                     'message': 'User logged in successfully',
#                     'token': token.key,
#                     'user_id': user.id
#                 }, status=status.HTTP_200_OK)
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
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({
                    'message': 'User logged in successfully',
                    'token': token.key,
                    'user_id': user.id
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
