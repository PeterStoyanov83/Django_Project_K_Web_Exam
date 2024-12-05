from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from client_management.models import CustomUser
from django.utils import timezone
from schedule.models.calendars import Calendar
from schedule.models.events import Event


class Room(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    capacity = models.PositiveIntegerField(_("Capacity"))

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))
    lecturer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses_taught',
                                 verbose_name=_("Lecturer"))
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    calendar = models.OneToOneField(Calendar, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return self.title

    def available_seats(self):
        if not self.room:
            return 0
        approved_applications = self.applications.filter(status='approved').count()
        return max(0, self.room.capacity - approved_applications)

    def is_full(self):
        return self.available_seats() == 0

    def save(self, *args, **kwargs):
        if not self.calendar:
            self.calendar = Calendar.objects.create(name=f"Calendar for {self.title}")
        super().save(*args, **kwargs)


class TimeSlot(models.Model):
    DAY_CHOICES = [
        ('MON', _('Monday')),
        ('TUE', _('Tuesday')),
        ('WED', _('Wednesday')),
        ('THU', _('Thursday')),
        ('FRI', _('Friday')),
        ('SAT', _('Saturday')),
        ('SUN', _('Sunday')),
    ]
    day = models.CharField(_("Day"), max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField(_("Start Time"))
    end_time = models.TimeField(_("End Time"))

    class Meta:
        verbose_name = _("Time Slot")
        verbose_name_plural = _("Time Slots")
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.get_day_display()} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"


class CourseSchedule(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', _('Scheduled')),
        ('CANCELLED', _('Cancelled')),
        ('COMPLETED', _('Completed')),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules', verbose_name=_("Course"))
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_("Room"))
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, verbose_name=_("Time Slot"))
    date = models.DateField(_("Date"))
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    event = models.OneToOneField(Event, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _("Course Schedule")
        verbose_name_plural = _("Course Schedules")
        ordering = ['date', 'time_slot__start_time']

    def __str__(self):
        return f"{self.course.title} - {self.date} {self.time_slot}"

    def clean(self):
        if self.room and self.time_slot and self.date:
            if CourseSchedule.objects.filter(
                    room=self.room,
                    time_slot=self.time_slot,
                    date=self.date
            ).exclude(pk=self.pk).exists():
                raise ValidationError(_('This room is already booked for the given time slot and date.'))
        if self.room and self.course and self.course.room and self.course.room.capacity < self.room.capacity:
            raise ValidationError(_('The course capacity exceeds the room capacity.'))

    def save(self, *args, **kwargs):
        self.clean()
        if not self.event:
            self.event = Event.objects.create(
                start=timezone.make_aware(timezone.datetime.combine(self.date, self.time_slot.start_time)),
                end=timezone.make_aware(timezone.datetime.combine(self.date, self.time_slot.end_time)),
                title=f"{self.course.title} - {self.room.name}",
                calendar=self.course.calendar
            )
        super().save(*args, **kwargs)


class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings', verbose_name=_("User"))
    course_schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE, related_name='bookings',
                                        verbose_name=_("Course Schedule"))
    booking_date = models.DateTimeField(_("Booking Date"), auto_now_add=True)

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")
        unique_together = ['user', 'course_schedule']

    def __str__(self):
        return f"{self.user.username} - {self.course_schedule}"


class CourseApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='course_applications')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='pending')
    application_date = models.DateTimeField(_("Application Date"), default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.get_status_display()})"
