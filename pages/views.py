from django.shortcuts import render
from course_management.models import Course

def home(request):
    featured_courses = Course.objects.all()[:3]
    return render(request, 'pages/home.html', {'featured_courses': featured_courses})

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return render(request, 'pages/contact.html')

