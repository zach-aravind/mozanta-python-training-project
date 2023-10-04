from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render

from . import serializers

User = get_user_model()


class UserRegistrationAPIView(GenericAPIView):
    """
    Endpoint to create a user.
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}

        return Response(data, status=HTTP_201_CREATED)


class UserLoginAPIView(GenericAPIView):
    """
    Endpoint to log in the existing user and authenticate.
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = serializers.CustomUserSerializer(user)
        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        data = serializer.data
        data["tokens"] = {"refresh": refresh_token, "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)


class UserAPIView(RetrieveUpdateAPIView):
    """
    Endpoint to get user details
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CustomUserSerializer

    def get_object(self):
        return self.request.user


def home_view(request):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    page_title = "Welcome to My Blog"
    return render(request, 'users/index.html', {'page_title': page_title})
