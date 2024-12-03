from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    phone_number = models.CharField(_("Phone Number"), max_length=15, blank=True)
    address = models.TextField(_("Address"), blank=True)
    date_of_birth = models.DateField(_("Date of Birth"), null=True, blank=True)
    profile_picture = models.ImageField(_("Profile Picture"), upload_to='profile_pictures/', null=True, blank=True)

    class Meta:
        verbose_name = _("Custom User")
        verbose_name_plural = _("Custom Users")

    def __str__(self):
        return self.username

    @property
    def client(self):
        try:
            return self.client_profile
        except Client.DoesNotExist:
            return None

    def is_client(self):
        return hasattr(self, 'client_profile')

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client_profile')
    company_name = models.CharField(_("Company Name"), max_length=100)
    industry = models.CharField(_("Industry"), max_length=50)
    registration_date = models.DateTimeField(_("Registration Date"), auto_now_add=True)

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __str__(self):
        return f"{self.user.username} - {self.company_name}"

def client_file_path(instance, filename):
    return f'client_files/{instance.client.user.username}/{filename}'

class ClientFile(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(_("File"), upload_to=client_file_path)
    upload_date = models.DateTimeField(_("Upload Date"), auto_now_add=True)

    class Meta:
        verbose_name = _("Client File")
        verbose_name_plural = _("Client Files")

    def __str__(self):
        return f"{self.client.user.username} - {self.file_name}"

    @property
    def file_name(self):
        return os.path.basename(self.file.name)

    @property
    def file_type(self):
        return self.file_name.split('.')[-1] if '.' in self.file_name else ''

class Laptop(models.Model):
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('maintenance', _('Maintenance')),
        ('retired', _('Retired'))
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='laptops')
    brand = models.CharField(_("Brand"), max_length=50)
    model = models.CharField(_("Model"), max_length=50)
    serial_number = models.CharField(_("Serial Number"), max_length=50, unique=True)
    purchase_date = models.DateField(_("Purchase Date"))
    warranty_end_date = models.DateField(_("Warranty End Date"))
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        verbose_name = _("Laptop")
        verbose_name_plural = _("Laptops")

    def __str__(self):
        return f"{self.brand} {self.model} - {self.client.user.username}"

class CourseApplication(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='client_course_applications')
    course = models.ForeignKey('course_management.Course', on_delete=models.CASCADE, related_name='client_applications')
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
                              default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Course Application")
        verbose_name_plural = _("Course Applications")

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

