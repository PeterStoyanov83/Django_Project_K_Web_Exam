from django.core.mail import send_mail
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Send a test email to verify email configuration'

    def handle(self, *args, **kwargs):
        try:
            send_mail(
                subject="Test Email",
                message="This is a test email from Django.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS("Test email sent successfully."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to send test email: {e}"))
