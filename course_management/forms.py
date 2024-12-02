from django import forms
from .models import Course, CourseSchedule, Booking


class CourseForm(forms.ModelForm):
    schedule_status = forms.ChoiceField(choices=CourseSchedule.STATUS_CHOICES, required=False)

    class Meta:
        model = Course
        fields = ['title', 'description', 'capacity', 'lecturer', 'schedule_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # If editing an existing course, get the latest schedule status
            latest_schedule = self.instance.schedules.order_by('-date').first()
            if latest_schedule:
                self.fields['schedule_status'].initial = latest_schedule.status
        self.fields['schedule_status'].widget.attrs.update({'class': 'form-select'})


class CourseScheduleForm(forms.ModelForm):
    class Meta:
        model = CourseSchedule
        fields = ['room', 'time_slot', 'date', 'status']


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
