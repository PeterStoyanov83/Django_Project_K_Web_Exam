from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from client_management.models import CustomUser
from course_management.models import Course, CourseSchedule, Room, CourseApplication, TimeSlot, Booking
from django.utils import timezone
from datetime import time

User = get_user_model()


class CourseManagementViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(username='staffuser', password='12345', is_staff=True)
        self.normal_user = User.objects.create_user(username='normaluser', password='12345')
        self.room = Room.objects.create(name='Test Room', capacity=30)
        self.time_slot = TimeSlot.objects.create(day='MON', start_time=time(9, 0), end_time=time(11, 0))
        self.course = Course.objects.create(
            title='Test Course',
            description='This is a test course',
            lecturer=self.staff_user,
            room=self.room,
            capacity=20
        )
        self.schedule = CourseSchedule.objects.create(
            course=self.course,
            room=self.room,
            time_slot=self.time_slot,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=7),
            days_of_week="0,2,4",
            status='SCHEDULED'
        )

    def test_course_list_view(self):
        response = self.client.get(reverse('course_management:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_management/course_list.html')
        self.assertContains(response, 'Test Course')

    def test_schedule_view(self):
        response = self.client.get(reverse('course_management:schedule'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_management/schedule.html')
        self.assertContains(response, 'Test Room')
        self.assertContains(response, 'Test Course')

    def test_course_create_view_staff(self):
        self.client.login(username='staffuser', password='12345')
        response = self.client.get(reverse('course_management:course_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_management/course_form.html')

    def test_course_create_view_normal_user(self):
        self.client.login(username='normaluser', password='12345')
        response = self.client.get(reverse('course_management:course_create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_course_update_view_staff(self):
        self.client.login(username='staffuser', password='12345')
        response = self.client.get(reverse('course_management:course_update', args=[self.course.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_management/course_form.html')

    def test_course_detail_view(self):
        response = self.client.get(reverse('course_management:course_detail', args=[self.course.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_management/course_detail.html')
        self.assertContains(response, 'Test Course')

    def test_apply_for_course_authenticated(self):
        self.client.login(username='normaluser', password='12345')
        response = self.client.post(reverse('course_management:apply_for_course', args=[self.course.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful application
        self.assertTrue(CourseApplication.objects.filter(user=self.normal_user, course=self.course).exists())

    def test_apply_for_course_unauthenticated(self):
        response = self.client.get(reverse('course_management:apply_for_course', args=[1]))
        self.assertEqual(response.status_code, 403)  # Directly check status code

    def test_course_delete_view_staff(self):
        self.client.login(username='staffuser', password='12345')
        response = self.client.post(reverse('course_management:course_delete', args=[self.course.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Course.objects.filter(pk=self.course.pk).exists())

    def test_admin_course_applications_staff(self):
        self.client.login(username='staffuser', password='12345')
        response = self.client.get(reverse('course_management:admin_course_applications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_management/admin_course_applications.html')

    def test_admin_course_applications_normal_user(self):
        self.client.login(username='normaluser', password='12345')
        response = self.client.get(reverse('course_management:admin_course_applications'))
        self.assertEqual(response.status_code, 302)  # Redirect to course list

    def test_approve_course_application_staff(self):
        self.client.login(username='staffuser', password='12345')
        application = CourseApplication.objects.create(user=self.normal_user, course=self.course, status='pending')
        response = self.client.post(reverse('course_management:approve_course_application', args=[application.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after approval
        application.refresh_from_db()
        self.assertEqual(application.status, 'approved')

    def test_reject_course_application_staff(self):
        self.client.login(username='staffuser', password='12345')
        application = CourseApplication.objects.create(user=self.normal_user, course=self.course, status='pending')
        response = self.client.post(reverse('course_management:reject_course_application', args=[application.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after rejection
        application.refresh_from_db()
        self.assertEqual(application.status, 'rejected')

    def test_admin_panel_staff(self):
        self.client.login(username='staffuser', password='12345')
        response = self.client.get(reverse('course_management:admin_panel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_management/admin_panel.html')

    def test_admin_panel_normal_user(self):
        self.client.login(username='normaluser', password='12345')
        response = self.client.get(reverse('course_management:admin_panel'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_admin_courses_staff(self):
        self.client.login(username='staffuser', password='12345')
        response = self.client.get(reverse('course_management:admin_courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_management/admin_courses.html')

    def test_admin_lecturers_staff(self):
        self.client.login(username='staffuser', password='12345')
        response = self.client.get(reverse('course_management:admin_lecturers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_management/admin_lecturers.html')

    def test_admin_users_staff(self):
        self.client.login(username='staffuser', password='12345')
        response = self.client.get(reverse('course_management:admin_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_management/admin_users.html')

    def test_user_create_staff(self):
        self.client.login(username='staffuser', password='12345')
        response = self.client.get(reverse('course_management:user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_management/user_form.html')

    def test_user_edit_staff(self):
        self.client.login(username='staffuser', password='12345')
        response = self.client.get(reverse('course_management:user_edit', args=[self.normal_user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_management/user_form.html')
