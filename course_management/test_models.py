from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model

from client_management.models import CustomUser
from course_management.models import Room, TimeSlot, Course, CourseSchedule, CourseApplication, Booking
from datetime import time

User = get_user_model()


class RoomModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Room A", capacity=30)

    def test_room_str(self):
        self.assertEqual(str(self.room), "Room A (Capacity: 30)")

    def test_room_capacity(self):
        self.assertEqual(self.room.capacity, 30)


class TimeSlotModelTest(TestCase):
    def setUp(self):
        self.time_slot = TimeSlot.objects.create(
            day='MON',
            start_time=timezone.datetime.strptime("09:00", "%H:%M").time(),
            end_time=timezone.datetime.strptime("11:00", "%H:%M").time()
        )

    def test_time_slot_str(self):
        self.assertEqual(str(self.time_slot), "Monday 09:00 - 11:00")

    def test_time_slot_ordering(self):
        TimeSlot.objects.create(
            day='TUE',
            start_time=timezone.datetime.strptime("10:00", "%H:%M").time(),
            end_time=timezone.datetime.strptime("12:00", "%H:%M").time()
        )
        time_slots = TimeSlot.objects.all()
        self.assertEqual(time_slots[0].day, 'MON')
        self.assertEqual(time_slots[1].day, 'TUE')


class CourseModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Room A", capacity=30)
        self.lecturer = User.objects.create_user(username="lecturer", password="password")
        self.course = Course.objects.create(
            title="Test Course",
            description="Description",
            lecturer=self.lecturer,
            room=self.room,
            capacity=20
        )

    def test_course_str(self):
        self.assertEqual(str(self.course), "Test Course")

    def test_course_available_seats(self):
        self.assertEqual(self.course.available_seats(), 20)

        # Create approved applications
        for i in range(5):
            user = User.objects.create_user(username=f"student{i}", password="password")
            CourseApplication.objects.create(user=user, course=self.course, status='approved')

        self.assertEqual(self.course.available_seats(), 15)

    def test_course_is_full(self):
        self.assertFalse(self.course.is_full())

        # Fill up the course
        for i in range(20):
            user = User.objects.create_user(username=f"student{i}", password="password")
            CourseApplication.objects.create(user=user, course=self.course, status='approved')

        self.assertTrue(self.course.is_full())

    def test_course_calendar_creation(self):
        self.assertIsNotNone(self.course.calendar)
        self.assertEqual(self.course.calendar.name, f"Calendar for {self.course.title}")


class CourseScheduleModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Room A", capacity=30)
        self.lecturer = get_user_model().objects.create_user(username="lecturer", password="password")
        self.course = Course.objects.create(
            title="Test Course",
            description="Description",
            lecturer=self.lecturer,
            room=self.room,
            capacity=20
        )
        self.time_slot = TimeSlot.objects.create(
            day='MON',
            start_time=time(9, 0),
            end_time=time(11, 0)
        )

    def test_schedule_creation(self):
        start_date = timezone.now().date()
        end_date = start_date + timezone.timedelta(days=7)
        schedule = CourseSchedule.objects.create(
            course=self.course,
            room=self.room,
            time_slot=self.time_slot,
            start_date=start_date,
            end_date=end_date,
            days_of_week="0,2,4"
        )
        self.assertEqual(str(schedule), f"{self.course.title} - {start_date} to {end_date}")

    def test_schedule_clean(self):
        start_date = timezone.now().date()
        end_date = start_date + timezone.timedelta(days=7)
        schedule = CourseSchedule(
            course=self.course,
            room=self.room,
            time_slot=self.time_slot,
            start_date=start_date,
            end_date=end_date,
            days_of_week="0,2,4"
        )
        schedule.clean()  # This should not raise an exception

        # Test for room capacity validation
        small_room = Room.objects.create(name="Small Room", capacity=10)
        with self.assertRaises(ValidationError):
            invalid_schedule = CourseSchedule(
                course=self.course,
                room=small_room,
                time_slot=self.time_slot,
                start_date=start_date,
                end_date=end_date,
                days_of_week="0,2,4"
            )
            invalid_schedule.clean()

    def test_get_event_dates(self):
        start_date = timezone.datetime(2023, 5, 1).date()  # A Monday
        end_date = start_date + timezone.timedelta(days=13)  # Two weeks later
        schedule = CourseSchedule.objects.create(
            course=self.course,
            room=self.room,
            time_slot=self.time_slot,
            start_date=start_date,
            end_date=end_date,
            days_of_week="0,2,4"  # Monday, Wednesday, Friday
        )
        event_dates = schedule.get_event_dates()
        expected_dates = [
            timezone.datetime(2023, 5, 1).date(),
            timezone.datetime(2023, 5, 3).date(),
            timezone.datetime(2023, 5, 5).date(),
            timezone.datetime(2023, 5, 8).date(),
            timezone.datetime(2023, 5, 10).date(),
            timezone.datetime(2023, 5, 12).date(),
        ]
        self.assertEqual(event_dates, expected_dates)


class CourseApplicationModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Room A", capacity=30)
        self.lecturer = User.objects.create_user(username="lecturer", password="password")
        self.course = Course.objects.create(
            title="Test Course",
            description="Description",
            lecturer=self.lecturer,
            room=self.room,
            capacity=20
        )
        self.student = User.objects.create_user(username="student", password="password")
        self.application = CourseApplication.objects.create(
            user=self.student,
            course=self.course
        )

    def test_course_application_str(self):
        self.assertEqual(str(self.application), f"{self.student.username} - {self.course.title} (Pending)")

    def test_course_application_default_status(self):
        self.assertEqual(self.application.status, 'pending')

    def test_course_application_status_choices(self):
        self.application.status = 'approved'
        self.application.save()
        self.assertEqual(self.application.get_status_display(), 'Approved')

        self.application.status = 'rejected'
        self.application.save()
        self.assertEqual(self.application.get_status_display(), 'Rejected')


class BookingModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Room A", capacity=30)
        self.lecturer = User.objects.create_user(username="lecturer", password="password")
        self.student = User.objects.create_user(username="student", password="password")
        self.course = Course.objects.create(
            title="Test Course",
            description="Description",
            lecturer=self.lecturer,
            room=self.room,
            capacity=20
        )
        self.time_slot = TimeSlot.objects.create(
            day='MON',
            start_time=timezone.datetime.strptime("09:00", "%H:%M").time(),
            end_time=timezone.datetime.strptime("11:00", "%H:%M").time()
        )
        self.schedule = CourseSchedule.objects.create(
            course=self.course,
            room=self.room,
            time_slot=self.time_slot,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=7),
            days_of_week="0,2,4"
        )

    def test_booking_creation(self):
        booking = Booking.objects.create(user=self.student, course_schedule=self.schedule)
        self.assertEqual(str(booking), f"{self.student.username} - {self.course.title}")

    def test_booking_clean_cancelled_schedule(self):
        self.schedule.status = 'CANCELLED'
        self.schedule.save()
        with self.assertRaises(ValidationError):
            booking = Booking(user=self.student, course_schedule=self.schedule)
            booking.clean()
