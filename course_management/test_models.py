from django.test import TestCase
from django.utils.timezone import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from course_management.models import Room, TimeSlot, Course, CourseSchedule


class RoomModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Room A", capacity=30)

    def test_room_str(self):
        self.assertEqual(str(self.room), "Room A")


class TimeSlotModelTest(TestCase):
    def setUp(self):
        self.time_slot = TimeSlot.objects.create(day='MON', start_time=datetime.strptime("09:00", "%H:%M").time(),
                                                 end_time=datetime.strptime("11:00", "%H:%M").time())

    def test_time_slot_str(self):
        self.assertEqual(str(self.time_slot), "Monday 09:00 - 11:00")


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
