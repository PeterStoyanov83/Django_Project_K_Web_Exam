from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .tasks import send_contact_email
import logging
from celery.exceptions import OperationalError
from django.utils.html import strip_tags

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


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        client_ip = request.META.get('REMOTE_ADDR', '')
        cache_key = f'contact_form_{client_ip}'
        cache_value = cache.get(cache_key, 0)

        if cache_value >= 5:  # Limit to 5 submissions per hour
            messages.error(request, "Too many submissions. Please try again later.")
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return redirect('pages:contact')

        cache.set(cache_key, cache_value + 1, 3600)  # Set cache for 1 hour

        # Validate input
        if not all([name, email, message]):
            messages.error(request, "Please fill in all fields.")
            return redirect('pages:contact')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return redirect('pages:contact')

        try:
            # Render email content
            email_content = render_to_string('mail/contact_email.html', {
                'name': name,
                'email': email,
                'message': message,
            })

            contact_email = getattr(settings, 'CONTACT_EMAIL', None)
            if contact_email:
                try:
                    send_contact_email.delay(
                        subject=f"New contact form submission from {name}",
                        message=email_content,
                        recipient_list=[contact_email]
                    )
                    messages.success(request, "Your message has been sent successfully. We'll get back to you soon!")
                    logger.info(f"Email task queued successfully for {email}")
                except OperationalError as e:
                    messages.error(request, "We're experiencing technical difficulties. Please try again later.")
                    logger.error(f"Celery OperationalError for {email}. Error: {str(e)}")
                except Exception as e:
                    messages.error(request, "An error occurred while sending your message. Please try again later.")
                    logger.error(f"Failed to queue email task for {email}. Error: {str(e)}")
            else:
                messages.error(request, "Unable to send email at this time. Please try again later.")
                logger.error("CONTACT_EMAIL setting is not configured")

        except Exception as e:
            messages.error(request, "An error occurred while processing your message. Please try again later.")
            logger.error(f"Unexpected error in contact form for {email}. Error: {str(e)}")

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

