from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'location', 'agreement_status')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser

