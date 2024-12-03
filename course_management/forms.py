from django import forms
from .models import Course, CourseSchedule, Booking, Room, TimeSlot


class CourseForm(forms.ModelForm):
    schedule_status = forms.ChoiceField(choices=CourseSchedule.STATUS_CHOICES, required=False)
    room = forms.ModelChoiceField(queryset=Room.objects.all(), required=False)
    capacity = forms.ModelChoiceField(
        queryset=Room.objects.values_list('capacity', flat=True).distinct().order_by('capacity'),
        required=False,
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}))
    time_slot = forms.ModelChoiceField(queryset=TimeSlot.objects.all(), required=False)
    schedule_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Course
        fields = ['title', 'description', 'lecturer', 'capacity', 'room', 'time_slot', 'schedule_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'description': forms.Textarea(
                attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'rows': 4}),
            'lecturer': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'capacity': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].widget.attrs.update({'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'})
        self.fields['time_slot'].widget.attrs.update({'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'})
        self.fields['schedule_status'].widget.attrs.update(
            {'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'})
        self.fields['schedule_date'].widget.attrs.update(
            {'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'})

        if self.instance.pk:
            latest_schedule = self.instance.schedules.order_by('-date').first()
            if latest_schedule:
                self.fields['schedule_status'].initial = latest_schedule.status
                self.fields['room'].initial = latest_schedule.room
                self.fields['time_slot'].initial = latest_schedule.time_slot
                self.fields['schedule_date'].initial = latest_schedule.date

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        if room:
            cleaned_data['capacity'] = room.capacity
        return cleaned_data


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
