from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from course_management.models import Course, Room, TimeSlot, CourseSchedule, CourseApplication
from course_management.forms import CourseForm
from datetime import date, time

User = get_user_model()

class CourseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.course = Course.objects.create(
            title='Test Course',
            description='This is a test course',
            lecturer=self.user,
            capacity=30
        )

    def test_course_creation(self):
        self.assertIsInstance(self.course, Course)
        self.assertEqual(str(self.course), 'Test Course')

class CourseFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.room = Room.objects.create(name='Room A', capacity=20)
        self.time_slot = TimeSlot.objects.create(day='MON', start_time=time(9, 0), end_time=time(11, 0))

    def test_valid_course_form(self):
        form = CourseForm(data={
            'title': 'New Course',
            'description': 'Course Description',
            'lecturer': self.user.id,
            'room': self.room.id,
            'time_slot': self.time_slot.id,
            'schedule_date': '2024-12-03',
            'schedule_status': 'SCHEDULED'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_course_form(self):
        form = CourseForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
