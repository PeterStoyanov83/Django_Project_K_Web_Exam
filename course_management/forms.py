from django import forms
from client_management.models import CustomUser, Client
from .models import Course, CourseSchedule, Booking
from django.forms import inlineformset_factory


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'lecturer', 'room']

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        if room:
            # Set the course capacity to match the room capacity
            cleaned_data['capacity'] = room.capacity
        else:
            raise forms.ValidationError("Please select a room for the course.")
        return cleaned_data


class CourseScheduleForm(forms.ModelForm):
    class Meta:
        model = CourseSchedule
        fields = ["room", "time_slot", "date", "status"]

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get("room")
        course = self.instance.course if self.instance else None
        if room and course and course.room.capacity > room.capacity:
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


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number',
                  'profile_picture', 'user_type', 'is_staff', 'is_superuser',
                  'date_of_birth', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['company_name', 'industry']
