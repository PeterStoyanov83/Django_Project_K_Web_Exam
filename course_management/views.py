from client_management.models import CustomUser
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Course, CourseSchedule, Room, CourseApplication, TimeSlot, Booking
from .forms import CourseForm, CourseScheduleForm, BookingForm, UserForm
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import inlineformset_factory


def course_list(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'course_management/course_list.html', context)


def schedule(request):
    schedules = CourseSchedule.objects.all().select_related('course', 'room', 'time_slot')
    rooms = Room.objects.all()
    time_slots = TimeSlot.objects.all().order_by('day', 'start_time')

    # Restructure the schedule data
    schedule_matrix = []
    for time_slot in time_slots:
        row = {
            'time_slot': time_slot,
            'rooms': []
        }
        for room in rooms:
            room_schedules = [
                schedule for schedule in schedules
                if schedule.room_id == room.id and schedule.time_slot_id == time_slot.id
            ]
            row['rooms'].append({
                'room': room,
                'schedules': room_schedules
            })
        schedule_matrix.append(row)

    context = {
        'rooms': rooms,
        'schedule_matrix': schedule_matrix,
    }
    return render(request, 'course_management/schedule.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def course_create(request):
    CourseScheduleFormSet = inlineformset_factory(Course, CourseSchedule, form=CourseScheduleForm, extra=1)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        schedule_formset = CourseScheduleFormSet(request.POST)
        if form.is_valid() and schedule_formset.is_valid():
            course = form.save()
            schedules = schedule_formset.save(commit=False)
            for schedule in schedules:
                schedule.course = course
                schedule.save()
            messages.success(request, 'Course created successfully.')
            return redirect('course_management:course_detail', pk=course.pk)
        else:
            if not form.is_valid():
                messages.error(request, 'There are errors in the course form.')
            if not schedule_formset.is_valid():
                messages.error(request, 'There are errors in the schedule formset.')
    else:
        form = CourseForm()
        schedule_formset = CourseScheduleFormSet()

    return render(request, 'course_management/course_form.html', {
        'form': form,
        'schedule_formset': schedule_formset
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    CourseScheduleFormSet = inlineformset_factory(Course, CourseSchedule, form=CourseScheduleForm, extra=1,
                                                  can_delete=True)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        schedule_formset = CourseScheduleFormSet(request.POST, instance=course)
        if form.is_valid() and schedule_formset.is_valid():
            form.save()
            schedule_formset.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('course_management:course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
        schedule_formset = CourseScheduleFormSet(instance=course)
    return render(request, 'course_management/course_form.html',
                  {'form': form, 'schedule_formset': schedule_formset, 'course': course})


@staff_member_required
def admin_only_view(request):
    return render(request, '../templates/403.html')


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    schedules = course.schedules.all()
    user_application = None
    if request.user.is_authenticated:
        user_application = CourseApplication.objects.filter(user=request.user, course=course).first()
    context = {
        'course': course,
        'schedules': schedules,
        'user_application': user_application,
    }
    return render(request, 'course_management/course_detail.html', context)


@login_required
def apply_for_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if course.is_full():
        messages.error(request, "This course is full and not accepting new applications.")
        return redirect('course_management:course_detail', pk=course_id)

    existing_application = CourseApplication.objects.filter(user=request.user, course=course).first()
    if existing_application:
        messages.info(request, "You have already applied for this course.")
    else:
        CourseApplication.objects.create(user=request.user, course=course)
        messages.success(request, "Your application has been submitted successfully.")

    return redirect('course_management:course_detail', pk=course_id)


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully.')
        return redirect('course_management:course_list')
    return render(request, 'course_management/course_confirm_delete.html', {'course': course})


@login_required
def schedule_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.method == 'POST':
        form = CourseScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.course = course
            schedule.save()
            messages.success(request, 'Schedule created successfully.')
            return redirect('course_management:course_detail', pk=course.pk)
    else:
        form = CourseScheduleForm()
    return render(request, 'course_management/schedule_form.html', {'form': form, 'course': course})


@login_required
def schedule_update(request, pk):
    schedule = get_object_or_404(CourseSchedule, pk=pk)
    if request.method == 'POST':
        form = CourseScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Schedule updated successfully.')
            return redirect('course_management:course_detail', pk=schedule.course.pk)
    else:
        form = CourseScheduleForm(instance=schedule)
    return render(request, 'course_management/schedule_form.html', {'form': form, 'schedule': schedule})


@login_required
def schedule_delete(request, pk):
    schedule = get_object_or_404(CourseSchedule, pk=pk)
    if request.method == 'POST':
        course_pk = schedule.course.pk
        schedule.delete()
        messages.success(request, 'Schedule deleted successfully.')
        return redirect('course_management:course_detail', pk=course_pk)
    return render(request, 'course_management/schedule_confirm_delete.html', {'schedule': schedule})


@login_required
def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Booking created successfully.')
            return redirect('course_management:booking_list')
    else:
        form = BookingForm()
    return render(request, 'course_management/booking_form.html', {'form': form})


@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'course_management/booking_list.html', {'bookings': bookings})


@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('course_management:booking_list')
    return render(request, 'course_management/booking_confirm_cancel.html', {'booking': booking})


@login_required
def admin_course_applications(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('course_management:course_list')

    applications = CourseApplication.objects.filter(status='pending').order_by('-application_date')
    return render(request, 'course_management/admin_course_applications.html', {'applications': applications})


@login_required
def approve_course_application(request, application_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('course_management:course_list')

    application = get_object_or_404(CourseApplication, pk=application_id)
    if application.course.is_full():
        messages.error(request, "This course is full. The application cannot be approved.")
    else:
        application.status = 'approved'
        application.save()
        messages.success(request, f"Application for {application.user.username} has been approved.")

    return redirect('course_management:admin_course_applications')


@login_required
def reject_course_application(request, application_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('course_management:course_list')

    application = get_object_or_404(CourseApplication, pk=application_id)
    application.status = 'rejected'
    application.save()
    messages.success(request, f"Application for {application.user.username} has been rejected.")

    return redirect('course_management:admin_course_applications')


@user_passes_test(lambda u: u.is_staff)
def admin_panel(request):
    return render(request, 'course_management/admin_panel.html')


@staff_member_required
def admin_only_view(request):
    return render(request, '../templates/403.html')


@user_passes_test(lambda u: u.is_staff)
def admin_courses(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'course_management/admin_courses.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_lecturers(request):
    lecturers = CustomUser.objects.filter(is_staff=True)
    context = {
        'lecturers': lecturers,
    }
    return render(request, 'course_management/admin_lecturers.html', context)


@user_passes_test(lambda u: u.is_staff)
def lecturer_create(request):
    # Placeholder view for creating a new lecturer
    if request.method == 'POST':
        # Process form data here
        messages.success(request, 'Lecturer created successfully.')
        return redirect('course_management:admin_lecturers')
    return render(request, 'course_management/lecturer_form.html')


@user_passes_test(lambda u: u.is_staff)
def lecturer_edit(request, pk):
    # Placeholder view for editing a lecturer
    lecturer = CustomUser.objects.get(pk=pk)
    if request.method == 'POST':
        # Process form data here
        messages.success(request, 'Lecturer updated successfully.')
        return redirect('course_management:admin_lecturers')
    context = {
        'lecturer': lecturer,
    }
    return render(request, 'course_management/lecturer_form.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_users(request):
    users = CustomUser.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'course_management/admin_users.html', context)


@user_passes_test(lambda u: u.is_staff)
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            return redirect('course_management:admin_users')
    else:
        form = UserForm()

    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, 'course_management/user_form.html', context)


@user_passes_test(lambda u: u.is_staff)
def user_edit(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('course_management:admin_users')
    else:
        form = UserForm(instance=user)

    context = {
        'form': form,
        'is_edit': True,
        'user': user,
    }
    return render(request, 'course_management/user_form.html', context)
