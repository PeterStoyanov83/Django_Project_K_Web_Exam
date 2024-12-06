from django.test import TestCase
from course_management.forms import CourseScheduleForm
from course_management.models import Room, Course, TimeSlot, CourseSchedule
from django.contrib.auth import get_user_model
from django.utils.timezone import datetime


class CourseScheduleFormTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Room A", capacity=30)
        self.time_slot = TimeSlot.objects.create(
            day="MON",
            start_time=datetime.strptime("09:00", "%H:%M").time(),
            end_time=datetime.strptime("11:00", "%H:%M").time(),
        )
        self.lecturer = get_user_model().objects.create_user(username="lecturer", password="password")
        self.course = Course.objects.create(
            title="Test Course",
            description="Description",
            lecturer=self.lecturer,
            room=self.room,
        )
        self.schedule_instance = CourseSchedule(course=self.course, room=self.room, time_slot=self.time_slot)

    def test_schedule_form_valid(self):
        form = CourseScheduleForm(
            data={
                "room": self.room.pk,
                "time_slot": self.time_slot.pk,
                "date": "2024-12-10",
                "status": "SCHEDULED",
            },
            instance=self.schedule_instance,
        )
        self.assertTrue(form.is_valid())

    def test_schedule_form_invalid(self):
        form = CourseScheduleForm(
            data={"room": "", "time_slot": "", "date": "", "status": ""},
            instance=self.schedule_instance,
        )
        self.assertFalse(form.is_valid())
