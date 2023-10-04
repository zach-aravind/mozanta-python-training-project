from django.contrib.auth import authenticate
from rest_framework import serializers
import re
from django.contrib.auth import password_validation
from rest_framework.exceptions import ValidationError
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email")


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if "@" not in value:
            raise serializers.ValidationError("Email must contain the '@' symbol.")

        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long.")

        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter.")

        if not any(char.islower() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter.")

        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one digit.")

        special_characters = "!@#$%^&*()_+{}[]:;<>,.?~\\-"
        if not any(char in special_characters for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one special character.")

        try:
            password_validation.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for log in.
    """
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long.")

        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter.")

        if not any(char.islower() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter.")

        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one digit.")

        special_characters = "!@#$%^&*()_+{}[]:;<>,.?~\\-"
        if not any(char in special_characters for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one special character.")

        return value

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

