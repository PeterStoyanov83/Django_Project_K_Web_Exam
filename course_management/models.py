from django.db import models
from client_management.models import Client

class Course(models.Model):
    PLATFORM_CHOICES = [
        ('online', 'Online'),
        ('in_person', 'In-Person'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    clients = models.ManyToManyField(Client)

    def __str__(self):
        return self.name

class CourseSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)
    time_slot = models.TimeField()

    def __str__(self):
        return f"{self.course.name} - {self.day_of_week} {self.time_slot}"

class Resource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    room = models.CharField(max_length=50)
    seat = models.CharField(max_length=10)

    class Meta:
        unique_together = ('course', 'room', 'seat')

    def __str__(self):
        return f"{self.course.name} - {self.client.name} - Room: {self.room}, Seat: {self.seat}"

