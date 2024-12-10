from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Course, CourseSchedule, Booking
from client_management.models import CustomUser
from django.core.exceptions import ValidationError


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'lecturer', 'room', 'capacity']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or title.strip() == '':
            raise ValidationError('Title cannot be empty or consist only of spaces.')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description or description.strip() == '':
            raise ValidationError('Description cannot be empty or consist only of spaces.')
        return description


class CourseScheduleForm(forms.ModelForm):
    days_of_week = forms.MultipleChoiceField(
        choices=[
            (0, _('Monday')),
            (1, _('Tuesday')),
            (2, _('Wednesday')),
            (3, _('Thursday')),
            (4, _('Friday')),
            (5, _('Saturday')),
            (6, _('Sunday'))
        ],
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = CourseSchedule
        fields = ['course', 'room', 'time_slot', 'start_date', 'end_date', 'days_of_week', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        days = cleaned_data.get('days_of_week')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError(_("End date must be after start date."))

        if days:
            cleaned_data['days_of_week'] = ','.join(days)

        return cleaned_data


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['course_schedule']

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('course_schedule'):
            raise forms.ValidationError(_('Course schedule is required.'))
        return cleaned_data


class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'phone_number',
                  'user_type', 'date_of_birth', 'address']
        widgets = {
            'password': forms.PasswordInput(),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
