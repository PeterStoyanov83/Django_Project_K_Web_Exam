from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm, LaptopForm, ClientForm, CustomUserForm, \
    ClientFileForm
from .models import Client, Laptop, ClientFile
from course_management.models import Course, CourseApplication

from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def profile_edit(request):
    user = request.user
    try:
        client = user.client
    except Client.DoesNotExist:
        client = Client.objects.create(user=user)

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, request.FILES, instance=user)
        client_form = ClientForm(request.POST, instance=client)
        if user_form.is_valid() and client_form.is_valid():
            user_form.save()
            client_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('client_management:profile')
    else:
        user_form = CustomUserForm(instance=user)
        client_form = ClientForm(instance=client)

    context = {
        'user_form': user_form,
        'client_form': client_form,
    }
    return render(request, 'client_management/profile_edit.html', context)


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = ClientFileForm(request.POST, request.FILES)
        if form.is_valid():
            client_file = form.save(commit=False)
            client_file.client = request.user.client
            client_file.save()
            messages.success(request, 'File uploaded successfully.')
            return HttpResponseRedirect(reverse('client_management:profile'))
    return HttpResponseRedirect(reverse('client_management:profile'))


@login_required
def profile(request):
    try:
        client = request.user.client
    except Client.DoesNotExist:
        client = Client.objects.create(user=request.user)

    client_files = ClientFile.objects.filter(client=client)
    context = {
        'client': client,
        'client_files': client_files,
        'file_form': ClientFileForm(),
    }
    return render(request, 'client_management/profile.html', context)


@login_required
def laptop_list(request):
    laptops = Laptop.objects.filter(client=request.user.client)
    return render(request, 'client_management/laptop_list.html', {'laptops': laptops})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful.')
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
                messages.success(request, f'Welcome back, {username}!')
                return redirect('client_management:profile')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'client_management/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('client_management:login')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'client_management/password_reset.html'
    email_template_name = 'client_management/password_reset_email.html'
    success_url = reverse_lazy('client_management:password_reset_done')


@login_required
def laptop_create(request):
    if request.method == 'POST':
        form = LaptopForm(request.POST)
        if form.is_valid():
            laptop = form.save(commit=False)
            laptop.client = request.user.client
            laptop.save()
            messages.success(request, 'Laptop created successfully.')
            return redirect('client_management:laptop_list')
    else:
        form = LaptopForm()
    return render(request, 'client_management/laptop_form.html', {'form': form, 'action': 'Create'})


@login_required
def laptop_update(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk, client=request.user.client)
    if request.method == 'POST':
        form = LaptopForm(request.POST, instance=laptop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laptop updated successfully.')
            return redirect('client_management:laptop_list')
    else:
        form = LaptopForm(instance=laptop)
    return render(request, 'client_management/laptop_form.html', {'form': form, 'action': 'Update'})


@login_required
def laptop_delete(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk, client=request.user.client)
    if request.method == 'POST':
        laptop.delete()
        messages.success(request, 'Laptop deleted successfully.')
        return redirect('client_management:laptop_list')
    return render(request, 'client_management/laptop_confirm_delete.html', {'laptop': laptop})


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = ClientFileForm(request.POST, request.FILES)
        if form.is_valid():
            client_file = form.save(commit=False)
            client_file.client = request.user.client
            client_file.save()
            messages.success(request, 'File uploaded successfully.')
    return redirect('client_management:profile')


@login_required
def delete_file(request, pk):
    file = get_object_or_404(ClientFile, pk=pk, client=request.user.client)
    file.delete()
    messages.success(request, 'File deleted successfully.')
    return redirect('client_management:profile')


@login_required
def apply_for_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = get_object_or_404(Course, id=course_id)
        CourseApplication.objects.create(user=request.user, course=course)
        messages.success(request, 'Course application submitted successfully.')
        return redirect('client_management:profile')
    courses = Course.objects.all()
    return render(request, '../client_management/templates/client_management/apply_for_course.html',
                  {'courses': courses})
