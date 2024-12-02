from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from course_management.models import Course
from django.conf import settings


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
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send email
        subject = f"New contact form submission from {name}"
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        try:
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully. We'll get back to you soon!")
        except Exception as e:
            messages.error(request, "An error occurred while sending your message. Please try again later.")

        return redirect('pages:contact')

    context = {
        'page_title': 'Contact Us'
    }
    return render(request, 'pages/contact.html', context)

