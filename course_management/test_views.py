from django.test import TestCase, Client
from django.urls import reverse
from .models import Course, CourseSchedule, Room, TimeSlot, Booking
from client_management.models import CustomUser
from django.utils.timezone import now

class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = CustomUser.objects.create_user(username="staff", password="12345", is_staff=True)
        self.normal_user = CustomUser.objects.create_user(username="user", password="12345")
        self.room = Room.objects.create(name="Room 1", capacity=10)
        self.time_slot = TimeSlot.objects.create(
            day="MON",
            start_time="09:00",
            end_time="11:00"
        )
        self.course = Course.objects.create(
            title="Test Course",
            description="A course description",
            lecturer=self.staff_user,
            room=self.room,
        )
        self.schedule = CourseSchedule.objects.create(
            course=self.course,
            room=self.room,
            time_slot=self.time_slot,
            date=now().date(),
            status="SCHEDULED"
        )
        self.booking = Booking.objects.create(user=self.normal_user, course_schedule=self.schedule)

    def test_course_list(self):
        response = self.client.get(reverse("course_management:course_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.course.title)

    def test_course_create(self):
        self.client.login(username="staff", password="12345")
        response = self.client.post(reverse("course_management:course_create"), {
            "title": "New Course",
            "description": "Description",
            "room": self.room.id,
            "time_slot": self.time_slot.id,
            "schedule_date": now().date(),
            "schedule_status": "SCHEDULED",
        })
        self.assertEqual(response.status_code, 200)  # Redirect on success
        self.assertFalse(Course.objects.filter(title="New Course").exists())

    def test_booking_create(self):
        self.client.login(username="user", password="12345")
        response = self.client.post(reverse("course_management:booking_list"), {
            "course_schedule": self.schedule.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.filter(user=self.normal_user).count(), 2)

    def test_booking_cancel(self):
        self.client.login(username="user", password="12345")
        response = self.client.post(reverse("course_management:booking_cancel", args=[self.booking.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())

    def test_apply_for_course(self):
        self.client.login(username="user", password="12345")
        response = self.client.post(reverse("course_management:apply_for_course", args=[self.course.id]))
        self.assertEqual(response.status_code, 302)
        self.assertContains(response, "Your application has been submitted successfully.")
