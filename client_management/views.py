from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Client, Laptop
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ClientForm, LaptopForm, ClientFileForm
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_management/client_list.html', {'clients': clients})

@login_required
def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'client_management/client_detail.html', {'client': client})

@login_required
def client_edit(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_management:client_detail', client_id=client.id)
    else:
        form = ClientForm(instance=client)
    return render(request, 'client_management/client_edit.html', {'form': form, 'client': client})

@login_required
def client_delete(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('client_management:client_list')
    return render(request, 'client_management/client_delete.html', {'client': client})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('client_management:profile')
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
                return redirect('client_management:profile')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'client_management/login.html', {'form': form})

@login_required
def profile(request):
    client, created = Client.objects.get_or_create(user=request.user)
    return render(request, 'client_management/profile.html', {'client': client})

@login_required
def laptop_list(request):
    laptops = Laptop.objects.all()
    return render(request, 'client_management/laptop_list.html', {'laptops': laptops})

@login_required
def laptop_detail(request, laptop_id):
    laptop = get_object_or_404(Laptop, id=laptop_id)
    return render(request, 'client_management/laptop_detail.html', {'laptop': laptop})

@login_required
def laptop_edit(request, laptop_id):
    laptop = get_object_or_404(Laptop, id=laptop_id)
    if request.method == 'POST':
        form = LaptopForm(request.POST, instance=laptop)
        if form.is_valid():
            form.save()
            return redirect('client_management:laptop_detail', laptop_id=laptop.id)
    else:
        form = LaptopForm(instance=laptop)
    return render(request, 'client_management/laptop_edit.html', {'form': form, 'laptop': laptop})

@login_required
def laptop_delete(request, laptop_id):
    laptop = get_object_or_404(Laptop, id=laptop_id)
    if request.method == 'POST':
        laptop.delete()
        return redirect('client_management:laptop_list')
    return render(request, 'client_management/laptop_delete.html', {'laptop': laptop})

@login_required
def client_file_upload(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientFileForm(request.POST, request.FILES)
        if form.is_valid():
            client_file = form.save(commit=False)
            client_file.client = client
            client_file.save()
            return redirect('client_management:client_detail', client_id=client.id)
    else:
        form = ClientFileForm()
    return render(request, 'client_management/client_file_upload.html', {'form': form, 'client': client})