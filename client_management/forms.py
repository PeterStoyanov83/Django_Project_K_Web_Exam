from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Client, Laptop, ClientFile


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number', 'user_type')


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'profile_picture', 'user_type',
                  'date_of_birth', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'profile_picture',
                  'user_type']
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }


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


class ClientFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }
