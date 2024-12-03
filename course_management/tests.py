from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Course, Room, TimeSlot, CourseSchedule, CourseApplication
from .forms import CourseForm
from datetime import date, time

User = get_user_model()


class CourseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.course = Course.objects.create(
            title='Test Course',
            description='This is a test course',
            lecturer=self.user,
            capacity=20
        )

    def test_course_creation(self):
        self.assertTrue(isinstance(self.course, Course))
        self.assertEqual(self.course.__str__(), self.course.title)

    def test_course_available_seats(self):
        self.assertEqual(self.course.available_seats(), 20)

    def test_course_is_full(self):
        self.assertFalse(self.course.is_full())


class CourseFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.room = Room.objects.create(name='Test Room', capacity=30)
        self.time_slot = TimeSlot.objects.create(day='MON', start_time=time(9, 0), end_time=time(11, 0))

    def test_course_form_valid_data(self):
        form = CourseForm(data={
            'title': 'New Course',
            'description': 'This is a new course',
            'lecturer': self.user.id,
            'capacity': 30,
            'room': self.room.id,
            'time_slot': self.time_slot.id,
            'schedule_date': date.today(),
            'schedule_status': 'SCHEDULED'
        })
        self.assertTrue(form.is_valid())

    def test_course_form_invalid_data(self):
        form = CourseForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)  # title, description, and lecturer are required


class CourseViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.course = Course.objects.create(
            title='Test Course',
            description='This is a test course',
            lecturer=self.user,
            capacity=20
        )
        self.course_url = reverse('course_management:course_detail', args=[self.course.id])

    def test_course_list_view(self):
        response = self.client.get(reverse('course_management:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_management/course_list.html')

    def test_course_detail_view(self):
        response = self.client.get(self.course_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_management/course_detail.html')

    def test_course_create_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('course_management:course_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_management/course_form.html')


class CourseIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.room = Room.objects.create(name='Test Room', capacity=30)
        self.time_slot = TimeSlot.objects.create(day='MON', start_time=time(9, 0), end_time=time(11, 0))

    def test_course_creation_and_scheduling(self):
        self.client.login(username='testuser', password='12345')

        # Create a new course
        course_data = {
            'title': 'Integration Test Course',
            'description': 'This is an integration test course',
            'lecturer': self.user.id,
            'capacity': 25,
            'room': self.room.id,
            'time_slot': self.time_slot.id,
            'schedule_date': date.today(),
            'schedule_status': 'SCHEDULED'
        }
        response = self.client.post(reverse('course_management:course_create'), data=course_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation

        # Check if the course was created
        course = Course.objects.get(title='Integration Test Course')
        self.assertIsNotNone(course)

        # Check if a course schedule was created
        schedule = CourseSchedule.objects.filter(course=course).first()
        self.assertIsNotNone(schedule)
        self.assertEqual(schedule.room, self.room)
        self.assertEqual(schedule.time_slot, self.time_slot)
        self.assertEqual(schedule.status, 'SCHEDULED')


class CourseApplicationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.course = Course.objects.create(
            title='Test Course',
            description='This is a test course',
            lecturer=self.user,
            capacity=20
        )

    def test_course_application_process(self):
        self.client.login(username='testuser', password='12345')

        # Apply for the course
        response = self.client.post(reverse('course_management:apply_for_course', args=[self.course.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful application

        # Check if the application was created
        application = CourseApplication.objects.filter(user=self.user, course=self.course).first()
        self.assertIsNotNone(application)
        self.assertEqual(application.status, 'pending')

        # Test application approval (assuming the user is staff)
        self.user.is_staff = True
        self.user.save()
        response = self.client.post(reverse('course_management:approve_course_application', args=[application.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after approval

        # Check if the application status was updated
        application.refresh_from_db()
        self.assertEqual(application.status, 'approved')

        # Check if the available seats were updated
        self.course.refresh_from_db()
        self.assertEqual(self.course.available_seats(), 19)

