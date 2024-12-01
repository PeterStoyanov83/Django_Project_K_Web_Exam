from django.shortcuts import render
from course_management.models import Course

def home(request):
    featured_courses = Course.objects.all()[:3]
    context = {
        'featured_courses': featured_courses,
        'page_title': 'Welcome to Project K'
    }
    return render(request, 'pages/home.html', context)

def about(request):
    context = {
        'page_title': 'About Us'
    }
    return render(request, 'pages/about.html', context)

def contact(request):
    context = {
        'page_title': 'Contact Us'
    }
    return render(request, 'pages/contact.html', context)

