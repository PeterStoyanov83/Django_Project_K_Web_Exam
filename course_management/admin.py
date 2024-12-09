from django.contrib import admin
from .models import Room, TimeSlot, Course, CourseSchedule, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'lecturer', 'room')
    search_fields = ('title', 'lecturer__username')

@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'room', 'time_slot', 'start_date', 'status')
    list_filter = ('status', 'start_date', 'room')
    search_fields = ('course__title', 'room__name')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'course_schedule', 'booking_date')
    list_filter = ('course_schedule__start_date', 'booking_date')
    search_fields = ('user__username', 'course_schedule__course__title')

