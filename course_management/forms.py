from django import forms
from .models import Course, Room, TimeSlot, CourseSchedule, Booking

from django.forms import inlineformset_factory




class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'lecturer', 'capacity']

    def clean(self):
        cleaned_data = super().clean()
        capacity = cleaned_data.get('capacity')
        if capacity is not None and capacity <= 0:
            raise forms.ValidationError("Capacity must be a positive number.")
        return cleaned_data

class CourseScheduleForm(forms.ModelForm):
    class Meta:
        model = CourseSchedule
        fields = ['room', 'time_slot', 'date', 'status']

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        course = self.instance.course if self.instance else None
        if room and course and course.capacity > room.capacity:
            raise forms.ValidationError("Course capacity cannot exceed room capacity.")
        return cleaned_data

CourseScheduleFormSet = inlineformset_factory(
    Course,
    CourseSchedule,
    form=CourseScheduleForm,
    extra=1,
    can_delete=True
)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['course_schedule']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['course_schedule'].queryset = CourseSchedule.objects.filter(status='SCHEDULED')

    def clean(self):
        cleaned_data = super().clean()
        course_schedule = cleaned_data.get('course_schedule')
        if course_schedule:
            if course_schedule.status != 'SCHEDULED':
                raise forms.ValidationError('This course is no longer available for booking.')
            if course_schedule.bookings.count() >= course_schedule.course.capacity:
                raise forms.ValidationError('This course is fully booked.')
            if Booking.objects.filter(course_schedule=course_schedule, user=self.user).exists():
                raise forms.ValidationError('You have already booked this course.')
        return cleaned_data
