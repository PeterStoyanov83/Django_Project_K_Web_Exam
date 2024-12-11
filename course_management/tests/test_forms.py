from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import time, timedelta

from client_management.models import CustomUser
from course_management.forms import CourseForm, CourseScheduleForm, BookingForm, UserForm
from course_management.models import Room, TimeSlot, Course, CourseSchedule

User = get_user_model()


class CourseFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.room = Room.objects.create(name='Test Room', capacity=30)

    def test_course_form_valid_data(self):
        form = CourseForm(data={
            'title': 'Test Course',
            'description': 'This is a test course',
            'lecturer': self.user.id,
            'room': self.room.id,
            'capacity': 20,
        })
        self.assertTrue(form.is_valid())

    def test_course_form_invalid_data(self):
        form = CourseForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)


class CourseScheduleFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.room = Room.objects.create(name='Test Room', capacity=30)
        self.course = Course.objects.create(
            title='Test Course',
            description='This is a test course',
            lecturer=self.user,
            room=self.room,
            capacity=20
        )
        self.time_slot = TimeSlot.objects.create(
            day='MON',
            start_time=time(9, 0),
            end_time=time(11, 0)
        )

    def test_course_schedule_form_valid_data(self):
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=7)
        form = CourseScheduleForm(data={
            'course': self.course.id,
            'room': self.room.id,
            'time_slot': self.time_slot.id,
            'start_date': start_date,
            'end_date': end_date,
            'days_of_week': ['0', '2', '4'],
            'status': 'SCHEDULED',
        })
        self.assertTrue(form.is_valid())


    def test_course_schedule_form_end_date_before_start_date(self):
        start_date = timezone.now().date()
        end_date = start_date - timedelta(days=1)
        form = CourseScheduleForm(data={
            'course': self.course.id,
            'room': self.room.id,
            'time_slot': self.time_slot.id,
            'start_date': start_date,
            'end_date': end_date,
            'days_of_week': ['0', '2', '4'],
            'status': 'SCHEDULED',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn('End date must be after start date.', form.errors['__all__'])

    def test_course_schedule_form_days_of_week_conversion(self):
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=7)
        form = CourseScheduleForm(data={
            'course': self.course.id,
            'room': self.room.id,
            'time_slot': self.time_slot.id,
            'start_date': start_date,
            'end_date': end_date,
            'days_of_week': ['0', '2', '4'],
            'status': 'SCHEDULED',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['days_of_week'], '0,2,4')


class BookingFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.room = Room.objects.create(name='Test Room', capacity=30)
        self.course = Course.objects.create(
            title='Test Course',
            description='This is a test course',
            lecturer=self.user,
            room=self.room,
            capacity=20
        )
        self.time_slot = TimeSlot.objects.create(
            day='MON',
            start_time=time(9, 0),
            end_time=time(11, 0)
        )
        self.schedule = CourseSchedule.objects.create(
            course=self.course,
            room=self.room,
            time_slot=self.time_slot,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=7),
            days_of_week='0,2,4',
            status='SCHEDULED'
        )


class UserFormTest(TestCase):
    def test_user_form_valid_data(self):
        form = UserForm(data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'confirm_password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890',
            'user_type': 'PRIVATE',
            'date_of_birth': '1990-01-01',
            'address': '123 Test St',
        })
        self.assertTrue(form.is_valid())

    def test_user_form_passwords_dont_match(self):
        form = UserForm(data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'confirm_password': 'differentpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890',
            'user_type': 'PRIVATE',
            'date_of_birth': '1990-01-01',
            'address': '123 Test St',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Passwords do not match', form.errors['__all__'][0])

    def test_user_form_invalid_data(self):
        form = UserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertGreater(len(form.errors), 0)
