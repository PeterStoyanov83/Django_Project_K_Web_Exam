from django.test import TestCase
from django.utils.timezone import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from course_management.models import Room, TimeSlot, Course, CourseSchedule, Booking, CourseApplication


class RoomModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Room A", capacity=30)

    def test_room_str(self):
        self.assertEqual(str(self.room), "Room A")

    def test_room_capacity(self):
        self.assertEqual(self.room.capacity, 30)


class TimeSlotModelTest(TestCase):
    def setUp(self):
        self.time_slot = TimeSlot.objects.create(day='MON', start_time=datetime.strptime("09:00", "%H:%M").time(),
                                                 end_time=datetime.strptime("11:00", "%H:%M").time())

    def test_time_slot_str(self):
        self.assertEqual(str(self.time_slot), "Monday 09:00 - 11:00")

    def test_time_slot_ordering(self):
        TimeSlot.objects.create(day='TUE', start_time=datetime.strptime("10:00", "%H:%M").time(),
                                end_time=datetime.strptime("12:00", "%H:%M").time())
        time_slots = TimeSlot.objects.all()
        self.assertEqual(time_slots[0].day, 'MON')
        self.assertEqual(time_slots[1].day, 'TUE')


class CourseModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Room A", capacity=30)
        self.lecturer = get_user_model().objects.create_user(username="lecturer", password="password")
        self.course = Course.objects.create(title="Test Course", description="Description", lecturer=self.lecturer,
                                            room=self.room)

    def test_course_str(self):
        self.assertEqual(str(self.course), "Test Course")

    def test_course_available_seats(self):
        self.assertEqual(self.course.available_seats(), 30)

        # Create approved applications
        for i in range(5):
            user = get_user_model().objects.create_user(username=f"student{i}", password="password")
            CourseApplication.objects.create(user=user, course=self.course, status='approved')

        self.assertEqual(self.course.available_seats(), 25)

    def test_course_is_full(self):
        self.assertFalse(self.course.is_full())

        # Fill up the course
        for i in range(30):
            user = get_user_model().objects.create_user(username=f"student{i}", password="password")
            CourseApplication.objects.create(user=user, course=self.course, status='approved')

        self.assertTrue(self.course.is_full())

    def test_course_calendar_creation(self):
        self.assertIsNotNone(self.course.calendar)
        self.assertEqual(self.course.calendar.name, f"Calendar for {self.course.title}")


class CourseScheduleModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Room A", capacity=30)
        self.lecturer = get_user_model().objects.create_user(username="lecturer", password="password")
        self.course = Course.objects.create(title="Test Course", description="Description", lecturer=self.lecturer,
                                            room=self.room)
        self.time_slot = TimeSlot.objects.create(day='MON', start_time=datetime.strptime("09:00", "%H:%M").time(),
                                                 end_time=datetime.strptime("11:00", "%H:%M").time())

    def test_schedule_creation(self):
        schedule = CourseSchedule.objects.create(course=self.course, room=self.room, time_slot=self.time_slot,
                                                 date=datetime.today().date())
        self.assertEqual(str(schedule),
                         f"{self.course.title} - {datetime.today().date()} Monday 09:00 - 11:00")

    def test_schedule_clean(self):
        CourseSchedule.objects.create(course=self.course, room=self.room, time_slot=self.time_slot,
                                      date=datetime.today().date())
        with self.assertRaises(ValidationError):
            duplicate_schedule = CourseSchedule(course=self.course, room=self.room, time_slot=self.time_slot,
                                                date=datetime.today().date())
            duplicate_schedule.clean()

    def test_schedule_event_creation(self):
        schedule = CourseSchedule.objects.create(course=self.course, room=self.room, time_slot=self.time_slot,
                                                 date=datetime.today().date())
        self.assertIsNotNone(schedule.event)
        self.assertEqual(schedule.event.title, f"{self.course.title} - {self.room.name}")


class BookingModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Room A", capacity=30)
        self.lecturer = get_user_model().objects.create_user(username="lecturer", password="password")
        self.student = get_user_model().objects.create_user(username="student", password="password")
        self.course = Course.objects.create(title="Test Course", description="Description", lecturer=self.lecturer,
                                            room=self.room)
        self.time_slot = TimeSlot.objects.create(day='MON', start_time=datetime.strptime("09:00", "%H:%M").time(),
                                                 end_time=datetime.strptime("11:00", "%H:%M").time())
        self.schedule = CourseSchedule.objects.create(course=self.course, room=self.room, time_slot=self.time_slot,
                                                      date=datetime.today().date())

    def test_booking_creation(self):
        booking = Booking.objects.create(user=self.student, course_schedule=self.schedule)
        self.assertEqual(str(booking), f"{self.student.username} - {self.schedule}")

    def test_booking_unique_constraint(self):
        Booking.objects.create(user=self.student, course_schedule=self.schedule)
        with self.assertRaises(ValidationError):
            duplicate_booking = Booking(user=self.student, course_schedule=self.schedule)
            duplicate_booking.full_clean()

    def test_course_application_creation(self):
        application = CourseApplication.objects.create(user=self.student, course=self.course)
        self.assertEqual(str(application), f"{self.student.username} - {self.course.title} (Pending)")

    def test_course_application_default_status(self):
        application = CourseApplication.objects.create(user=self.student, course=self.course)
        self.assertEqual(application.status, 'pending')

    def test_course_application_status_choices(self):
        application = CourseApplication.objects.create(user=self.student, course=self.course)
        application.status = 'approved'
        application.save()
        self.assertEqual(application.get_status_display(), 'Approved')

        application.status = 'rejected'
        application.save()
        self.assertEqual(application.get_status_display(), 'Rejected')
