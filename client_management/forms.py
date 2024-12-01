from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Client, Laptop

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address', 'date_of_birth')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['company_name', 'industry']

class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = ['brand', 'model', 'serial_number', 'purchase_date', 'warranty_end_date', 'status']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

