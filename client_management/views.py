from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ClientForm, LaptopForm
from .models import Client, Laptop, CustomUser





@login_required
def profile(request):
    client, created = Client.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_management:profile')
    else:
        form = ClientForm(instance=client)
    return render(request, 'client_management/profile.html', {'form': form, 'client': client})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pages:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'client_management/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pages:home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'client_management/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('pages:home')


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'client_management/password_reset_email.html'
    success_url = reverse_lazy('client_management:password_reset_done')
    template_name = 'client_management/password_reset.html'

@login_required
def laptop_list(request):
    laptops = Laptop.objects.filter(client=request.user.client)
    return render(request, 'client_management/laptop_list.html', {'laptops': laptops})


@login_required
def laptop_create(request):
    if request.method == 'POST':
        form = LaptopForm(request.POST)
        if form.is_valid():
            laptop = form.save(commit=False)
            laptop.client = request.user.client
            laptop.save()
            return redirect('client_management:profile')
    else:
        form = LaptopForm()
    return render(request, 'client_management/laptop_form.html', {'form': form, 'action': 'Create'})


@login_required
def laptop_update(request, pk):
    laptop = Laptop.objects.get(pk=pk)
    if request.method == 'POST':
        form = LaptopForm(request.POST, instance=laptop)
        if form.is_valid():
            form.save()
            return redirect('client_management:profile')
    else:
        form = LaptopForm(instance=laptop)
    return render(request, 'client_management/laptop_form.html', {'form': form, 'action': 'Update'})


@login_required
def laptop_delete(request, pk):
    laptop = Laptop.objects.get(pk=pk)
    if request.method == 'POST':
        laptop.delete()
        return redirect('client_management:profile')
    return render(request, 'client_management/laptop_confirm_delete.html', {'laptop': laptop})
