from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from signup_login.models import Message
from .serializers import MessageSerializer, UserLoginSerializers, UserRegistrationSerializers
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
# from signup_login.utils import get_tokens_for_user


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


class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializers(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                refresh = RefreshToken.for_user(user)
                login(request, user)

                response = Response({
                    'message': 'User logged in successfully',
                    'access': str(refresh.access_token),
                    'user_id': user.id
                }, status=status.HTTP_200_OK)

                response.set_cookie(
                    'refresh_token',
                    str(refresh),
                    httponly=True,
                    secure=False,
                    samesite='None',
                    max_age=3600 * 24,
                )

                return response
            else:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class UserLoginApiView(APIView):
#     def post(self, request):
#         serializer = UserLoginSerializers(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']
#             user = authenticate(request, email=email, password=password)
#             if user:
#                 # Use the function to get tokens
#                 tokens = get_tokens_for_user(user)
#                 response = Response({
#                     'message': 'User logged in successfully',
#                     'access': tokens['access'],
#                     'refresh': tokens['refresh'],
#                     'user_id': user.id
#                 }, status=status.HTTP_200_OK)

#                 response.set_cookie(
#                     'refresh_token',
#                     tokens['refresh'],
#                     httponly=True,
#                     secure=False,  # Set to True in production with HTTPS
#                     samesite='Lax',
#                 )

#                 return response
#             else:
#                 return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
