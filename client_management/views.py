from django.contrib.auth import authenticate, logout
from django.contrib.auth.views import PasswordResetView
from .forms import CustomUserCreationForm, CustomAuthenticationForm, LaptopForm, ClientFileForm, UserProfileForm, \
    ClientForm
from .models import Laptop, ClientFile
from course_management.models import Course, CourseApplication, CourseSchedule
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from .models import Client
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def profile(request):
    user_files = ClientFile.objects.filter(user=request.user).order_by('-uploaded_at')
    context = {
        'user': request.user,
        'client': request.user.client_profile if hasattr(request.user, 'client_profile') else None,
        'user_files': user_files,
    }
    return render(request, 'client_management/profile.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        client_form = ClientForm(request.POST, instance=request.user.client_profile) \
            if hasattr(request.user, 'client_profile') else None
        file_form = ClientFileForm(request.POST, request.FILES)

        if user_form.is_valid() and (not client_form or client_form.is_valid()) and file_form.is_valid():
            user_form.save()
            if client_form:
                client_form.save()
            if file_form.cleaned_data['file']:
                new_file = ClientFile(
                    user=request.user,
                    file=file_form.cleaned_data['file'],
                    uploaded_by=request.user
                )
                new_file.save()
                messages.success(request, 'File uploaded successfully.')
            messages.success(request, 'Profile updated successfully.')
            return redirect('client_management:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserProfileForm(instance=request.user)
        client_form = ClientForm(instance=request.user.client_profile) \
            if hasattr(request.user, 'client_profile') else None
        file_form = ClientFileForm()

    context = {
        'user_form': user_form,
        'client_form': client_form,
        'file_form': file_form,
    }
    return render(request, 'client_management/profile_edit.html', context)


@login_required
def delete_file(request, file_id):
    # Ensure the user has a client profile
    if hasattr(request.user, 'client_profile'):
        return HttpResponseForbidden("You do not have permission to delete this file.")

    # Ensure the file belongs to the logged-in user
    file = get_object_or_404(ClientFile, id=file_id, user=request.user)

    # Delete the file
    file.delete()
    messages.success(request, 'File deleted successfully.')
    return redirect('client_management:profile')


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = ClientFileForm(request.POST, request.FILES)
        if form.is_valid():
            client_file = form.save(commit=False)
            client_file.client = request.user.client_profile
            client_file.save()
            messages.success(request, 'File uploaded successfully.')
            return HttpResponseRedirect(reverse('client_management:profile'))
    return HttpResponseRedirect(reverse('client_management:profile'))


@login_required
def laptop_list(request):
    laptops = Laptop.objects.filter(client=request.user.client_profile)
    return render(request, 'client_management/laptop_list.html', {'laptops': laptops})


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'client_management/register.html'
    success_url = reverse_lazy('client_management:login')

    def form_valid(self, form):
        user = form.save()
        Client.objects.create(user=user)
        login(self.request, user)
        messages.success(self.request, 'Registration successful.')
        return super().form_valid(form)


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
            laptop.client = request.user.client_profile
            laptop.save()
            messages.success(request, 'Laptop created successfully.')
            return redirect('client_management:laptop_list')
    else:
        form = LaptopForm()
    return render(
        request,
        'client_management/laptop_form.html',
        {'form': form, 'action': 'Create'}
    )


@login_required
def laptop_update(request, pk):
    laptop = get_object_or_404(
        Laptop,
        pk=pk,
        client=request.user.client
    )
    if request.method == 'POST':
        form = LaptopForm(request.POST, instance=laptop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laptop updated successfully.')
            return redirect('client_management:laptop_list')
    else:
        form = LaptopForm(instance=laptop)
    return render(
        request,
        'client_management/laptop_form.html',
        {'form': form, 'action': 'Update'}
    )


@login_required
def laptop_delete(request, pk):
    laptop = get_object_or_404(
        Laptop,
        pk=pk,
        client=request.user.client
    )
    if request.method == 'POST':
        laptop.delete()
        messages.success(
            request,
            'Laptop deleted successfully.'
        )
        return redirect('client_management:laptop_list')
    return render(
        request,
        'client_management/laptop_confirm_delete.html',
        {'laptop': laptop}
    )


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = ClientFileForm(request.POST, request.FILES)
        if form.is_valid():
            client_file = form.save(commit=False)
            client_file.client = request.user.client_profile
            client_file.save()
            messages.success(request, 'File uploaded successfully.')
    return redirect('client_management:profile')



@login_required
def apply_for_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = get_object_or_404(
            Course,
            id=course_id
        )
        CourseApplication.objects.create(
            user=request.user,
            course=course
        )
        messages.success(request, 'Course application submitted successfully.')
        return redirect('client_management:profile')
    courses = Course.objects.all()
    return render(
        request,
        '../client_management/templates/client_management/apply_for_course.html',
        {'courses': courses})


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
