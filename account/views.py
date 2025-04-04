from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from knox.models import AuthToken
from knox.views import LogoutView, LogoutAllView, LoginView
from .auth import CookieTokenAuthentication as TokenAuthentication

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from .models import Profile
from .serializers import ProfileSerializer, ProfileUpdateSerializer, UserUpdateSerializer


class UserLogoutView(LogoutView):
    """
    Custom Logout View extending the Knox LogoutView, using the CookieTokenAuthentication
    """
    authentication_classes = (TokenAuthentication,)

    def post(self, request, format=None):
        response = super().post(request, format=None)
        response.delete_cookie('auth_token')
        return response


class UserLogoutAllView(LogoutAllView):
    """
    Custom LogoutAll View extending the Knox LogoutAllView, using the CookieTokenAuthentication
    """
    authentication_classes = (TokenAuthentication,)

    def post(self, request, format=None):
        response = super().post(request, format=None)
        response.delete_cookie('auth_token')
        return response


class GoogleAuthView(LoginView):
    """
    Authenticates the user using Firebase OAuth2.0.

    The view receives an ID token from the frontend and verifies it using the Google API.

    If the token is valid, the view creates a new user or updates an existing one and generates a Knox token.
    """
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request):
        id_token_str = request.data.get('id_token')
        print(id_token_str)
        if not id_token_str:
            return Response({'error': 'ID token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # print(f"GOOGLE CLIENT ID: {settings.GOOGLE_CLIENT_ID}")
            idinfo = id_token.verify_firebase_token(
                id_token_str, google_requests.Request()
            )
            # settings.GOOGLE_CLIENT_ID
            google_id = idinfo['sub']
            email = idinfo.get('email')
            name = idinfo.get('name')
            picture = idinfo.get('picture')

            print(google_id, email, name, picture)
            try:
                user = User.objects.get(username=email)
            except User.DoesNotExist:
                user = User(username=email, email=email)
                user.set_unusable_password()
                if name:
                    full_name = name.split(' ')
                    if len(full_name) > 1:
                        user.last_name = full_name[-1]
                        user.first_name = ' '.join(full_name[:-1])
                    else:
                        user.first_name = name
                user.save()

            # Update or create Profile
            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                profile.google_id = google_id
                profile.picture = picture
                profile.save()

            login(request, user)
            response = super().post(request, format=None)
            token = response.data["token"]
            expiry = response.data["expiry"]
            del response.data['token']

            serializer = ProfileSerializer(profile)
            response = Response(serializer.data, status=status.HTTP_200_OK)
            # TODO: set secure=True in production
            response.set_cookie('auth_token', token,
                                httponly=True, samesite="None", secure=True, expires=expiry)
            # partitioned=True)
            print(token)
            return response

        except ValueError as e:
            print(e)
            return Response({'error': 'Invalid ID token'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    Returns the user's profile information.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        request.data['user'] = user.id
        serializer = ProfileUpdateSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_serializer = UserUpdateSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({**serializer.data, **user_serializer.data}, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HardcodedLoginView(APIView):
    """
    Simple view that hardcodes a username and password, 
    authenticates the user and returns a Knox token.
    """
    authentication_classes = []  # Disable authentication for this view
    permission_classes = []  # Disable permission for this view

    def post(self, request, *args, **kwargs):
        hardcoded_username = "darpan"
        hardcoded_password = "darpan"

        user = authenticate(username=hardcoded_username,
                            password=hardcoded_password)

        if user is not None:
            _, token = AuthToken.objects.create(user)
            return Response({
                "token": token
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)
