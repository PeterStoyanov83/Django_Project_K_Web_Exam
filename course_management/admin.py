from django.contrib import admin
from .models import Course, CourseSchedule, Resource

admin.site.register(Course)
admin.site.register(CourseSchedule)
admin.site.register(Resource)

