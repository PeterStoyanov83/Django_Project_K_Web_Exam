from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Client, Laptop, ClientFile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'location', 'agreement_status')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['company_name', 'contact_person', 'phone_number', 'address']

class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = ['identifier', 'model', 'serial_number', 'status', 'client', 'assigned_date', 'return_date']

class ClientFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ['file', 'file_name', 'file_type']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'location', 'agreement_status']