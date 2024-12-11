from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Direct Test Subject',
    'This is a direct test email body.',
    settings.EMAIL_HOST_USER,
    ['p.stoyanov@craftgenie.ai'],  # Replace with your recipient email
    fail_silently=False,
)