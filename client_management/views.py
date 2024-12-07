import os

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm, LaptopForm, ClientForm, CustomUserForm, \
    ClientFileForm
from .models import Client, Laptop, ClientFile
from course_management.models import Course, CourseApplication, CourseSchedule

from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def profile_edit(request):
    """
    Handles user profile editing, including user and client information updates.
    Supports switching between 'PRIVATE' and 'BUSINESS' user types.
    """
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        client = None

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, request.FILES, instance=request.user)
        client_form = ClientForm(request.POST, instance=client) if client else ClientForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            old_user_type = user.user_type
            new_user_type = user_form.cleaned_data['user_type']

            # Handle user type changes
            if old_user_type != new_user_type:
                user.user_type = new_user_type
                if new_user_type == 'BUSINESS':
                    if not client:
                        client = Client(user=user)
                    client_form = ClientForm(request.POST, instance=client)
                elif new_user_type == 'PRIVATE' and client:
                    client.delete()
                    client = None

            user.save()

            # Save client form if the user type is BUSINESS
            if client and new_user_type == 'BUSINESS':
                if client_form.is_valid():
                    client = client_form.save(commit=False)
                    client.user = user
                    client.save()
                else:
                    messages.error(request, "Error saving client information.")

            messages.success(request, "Profile updated successfully.")
            return redirect('client_management:profile')
        else:
            messages.error(request, "Error updating user profile.")

    else:
        user_form = CustomUserForm(instance=request.user)
        client_form = ClientForm(instance=client) if client else None

    # Ensure that the GET request always returns a response
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

    # Add filename to each file object
    for file in client_files:
        file.filename = os.path.basename(file.file.name)

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
def delete_file(request, file_id):
    file = get_object_or_404(ClientFile, id=file_id, client=request.user.client)
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


class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 302 and not request.user.is_authenticated:
            # Check if the redirect is to a page that requires authentication
            redirect_url = response.url
            if any(url in redirect_url for url in ['/profile/', '/course/', '/admin/']):
                messages.error(request, "Not allowed! Please log in first.")
                return redirect(reverse('pages:home'))

        return response


@login_required
def my_schedule(request):
    approved_applications = CourseApplication.objects.filter(
        user=request.user,
        status='approved'
    ).select_related('course')

    course_ids = approved_applications.values_list('course_id', flat=True)
    schedules = CourseSchedule.objects.filter(
        course_id__in=course_ids
    ).select_related('course', 'room', 'time_slot')

    context = {
        'schedules': schedules,
    }
    return render(request, 'client_management/my_schedule.html', context)
