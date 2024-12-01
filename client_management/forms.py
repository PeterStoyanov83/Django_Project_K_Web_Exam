from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Client, Laptop, ClientFile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address', 'date_of_birth', 'profile_picture')


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['company_name', 'industry']


class ClientFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'accept': '.pdf,.doc,.docx'})
        }


class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = ['brand', 'model', 'serial_number', 'purchase_date', 'warranty_end_date', 'status']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_end_date': forms.DateInput(attrs={'type': 'date'}),
        }
