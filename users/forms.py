from django import forms



from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import CustomUser
from django.contrib.auth import authenticate


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')
