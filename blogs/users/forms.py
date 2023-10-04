from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new user using the CustomUser model.
    """
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    """
     Form for changing user information for the CustomUser model.
    """
    class Meta:
        model = CustomUser
        fields = ("email",)
