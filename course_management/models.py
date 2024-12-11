from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from client_management.models import CustomUser
from django.utils import timezone
from schedule.models import Calendar, Event
from datetime import datetime, time, timedelta


class Lecturer(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    courses = models.ManyToManyField('Course', related_name='lecturers', blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(
        _("Title"),
        max_length=200
    )
    description = models.TextField(_("Description"))
    lecturer = models.ForeignKey(
        'course_management.Lecturer',
        on_delete=models.CASCADE,
        related_name='assigned_courses',  # Changed to prevent clash
        verbose_name=_("Lecturer")
    )
    room = models.ForeignKey(
        to='Room',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )
    calendar = models.OneToOneField(
        to=Calendar,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    capacity = models.PositiveIntegerField(
        _("Capacity"),
        default=20
    )

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return self.title

    def available_seats(self):
        if not self.room:
            return 0
        approved_applications = self.applications.filter(status='approved').count()
        return max(0, self.capacity - approved_applications)

    def is_full(self):
        return self.available_seats() == 0

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new or not self.calendar:
            from schedule.models import Calendar
            slug = f"course-{self.id}-calendar"
            self.calendar, created = Calendar.objects.get_or_create(
                slug=slug,
                defaults={'name': f"Calendar for {self.title}"}
            )
            if not created:
                self.calendar.name = f"Calendar for {self.title}"
                self.calendar.save()
            super().save(update_fields=['calendar'])

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
    day = models.CharField(
        _("Day"),
        max_length=3,
        choices=DAY_CHOICES
    )
    start_time = models.TimeField(_("Start Time"))
    end_time = models.TimeField(_("End Time"))

    class Meta:
        verbose_name = _("Time Slot")
        verbose_name_plural = _("Time Slots")
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.get_day_display()} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

class Room(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    capacity = models.PositiveIntegerField(_("Capacity"))

    def __str__(self):
        return f"{self.name} (Capacity: {self.capacity})"

class CourseSchedule(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', _('Scheduled')),
        ('CANCELLED', _('Cancelled')),
        ('COMPLETED', _('Completed')),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules', verbose_name=_("Course"))
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_("Room"))
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, verbose_name=_("Time Slot"))
    start_date = models.DateField(_("Start Date"), default=timezone.now)
    end_date = models.DateField(_("End Date"))
    days_of_week = models.CharField(_("Days of Week"), max_length=20, help_text="Comma-separated list of weekday numbers (0-6)")
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    event = models.OneToOneField(Event, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _("Course Schedule")
        verbose_name_plural = _("Course Schedules")
        ordering = ['start_date', 'time_slot__start_time']

    def __str__(self):
        return f"{self.course.title} - {self.start_date} to {self.end_date}"

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError(_('End date must be after start date.'))
        if self.room and self.course and self.room.capacity < self.course.capacity:
            raise ValidationError(_('The room capacity is less than the course capacity.'))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        self.create_or_update_events()

    def create_or_update_events(self):
        if self.event:
            self.event.delete()

        if self.time_slot and isinstance(self.time_slot.start_time, time):
            event_dates = self.get_event_dates()
            for date in event_dates:
                try:
                    start = timezone.make_aware(datetime.combine(date, self.time_slot.start_time))
                    end = timezone.make_aware(datetime.combine(date, self.time_slot.end_time))
                    Event.objects.create(
                        start=start,
                        end=end,
                        title=f"{self.course.title} - {self.room.name}",
                        calendar=self.course.calendar
                    )
                except Exception as e:
                    print(f"Error creating event: {e}")
        else:
            print("Invalid time_slot or start_time")

    def get_event_dates(self):
        if isinstance(self.days_of_week, list):
            days = [int(day) for day in self.days_of_week]
        else:
            days = [int(day) for day in self.days_of_week.split(',')]
        current_date = self.start_date
        event_dates = []
        while current_date <= self.end_date:
            if current_date.weekday() in days:
                event_dates.append(current_date)
            current_date += timedelta(days=1)
        return event_dates

class CourseApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
    ]
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='course_applications')
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    application_date = models.DateTimeField(
        _("Application Date"),
        default=timezone.now
    )

    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.get_status_display()})"

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    course_schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(_("Booking Date"), auto_now_add=True)
    status = models.CharField(_("Status"), max_length=20, choices=[
        ('confirmed', _('Confirmed')),
        ('cancelled', _('Cancelled')),
    ], default='confirmed')

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")
        unique_together = ['user', 'course_schedule']

    def __str__(self):
        return f"{self.user.username} - {self.course_schedule.course.title}"

    def clean(self):
        if self.course_schedule and self.course_schedule.status != 'SCHEDULED':
            raise ValidationError(_('Cannot book a cancelled or completed course schedule.'))
        if self.course_schedule and self.course_schedule.course.is_full():
            raise ValidationError(_('This course is full.'))

