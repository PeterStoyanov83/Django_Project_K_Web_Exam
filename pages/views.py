from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import logging
from course_management.models import Course

logger = logging.getLogger(__name__)


def home(request):
    featured_courses = Course.objects.all().order_by('-id')[:3]
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


from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        # Validate input
        if not all([name, email, message]):
            messages.error(request, "Please fill in all fields.")
            return redirect('pages:contact')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return redirect('pages:contact')

        # Prepare email
        subject = f"New Contact Form Submission from {name}"
        email_message = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
        recipient_email = settings.CONTACT_EMAIL  # Ensure this is set in settings.py

        if not recipient_email:
            messages.error(request, "The contact email is not configured. Please try again later.")
            logger.error("CONTACT_EMAIL setting is missing.")
            return redirect('pages:contact')

        try:
            send_mail(
                subject=subject,
                message=email_message,
                from_email=email,  # Optionally, use a default email in settings
                recipient_list=[recipient_email],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
            logger.info(f"Email sent successfully from {email} to {recipient_email}.")
        except Exception as e:
            messages.error(request, "An error occurred while sending your message. Please try again later.")
            logger.error(f"Failed to send email. Error: {str(e)}")

        return redirect('pages:contact')

    context = {
        'page_title': 'Contact Us'
    }
    return render(request, 'pages/contact.html', context)


@login_required
def restricted_view(request):
    context = {
        'page_title': 'Restricted Area'
    }
    return render(request, '403.html', context)


def healthz(request):
    return JsonResponse({"status": "ok"}, status=200)
