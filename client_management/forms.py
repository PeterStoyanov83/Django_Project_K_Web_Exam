from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Laptop, Client, ClientFile

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = ['brand', 'model', 'serial_number', 'purchase_date', 'warranty_end_date', 'status']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'profile_picture': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['user']
        fields = ['company_name', 'industry']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'industry': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }

class ClientFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }