from loguru import logger
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers
from .models import *
from .utils import validate_password


class ListAllTasksView(generics.ListAPIView):
    """
    Endpoint for list all tasks in the db.
    """
    queryset = Tasks.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]


class CreateTaskView(generics.CreateAPIView):
    """
    Endpoint for creating a task against a user.
    """
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class RetrieveTaskView(generics.ListAPIView):
    """
    Endpoint to Retrieve tasks with a userId.
    """
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Tasks.objects.filter(user=user)


class UpdateTaskView(generics.UpdateAPIView):
    """
    Endpoint to update a task.
    """
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Tasks.objects.filter(user=user)


class DeleteTaskView(generics.DestroyAPIView):
    """
    Endpoint to delete a task.
    """
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Tasks.objects.filter(user=user)


class UserRegistrationAPIView(GenericAPIView):
    """
    An endpoint for the client to create a new User.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            password = serializer.validated_data.get("password")
            errors = validate_password(password)

            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            token = RefreshToken.for_user(user)
            data = serializer.data
            data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            logger.info('user registered successfully')
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as error:
            logger.error(str(error))
            return Response({str(error)}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing users using their email and password.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            serializer = serializers.CustomUserSerializer(user)
            token = RefreshToken.for_user(user)
            data = serializer.data
            data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            logger.info('login successfully')
            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            logger.error(str(error))
            return Response({str(error)}, status=status.HTTP_400_BAD_REQUEST)
