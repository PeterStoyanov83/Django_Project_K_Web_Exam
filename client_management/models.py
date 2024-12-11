from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    user_type = models.CharField(
        max_length=10,
        choices=[('PRIVATE', 'Private'), ('BUSINESS', 'Business')],
        default='PRIVATE'
    )
    address = models.TextField(
        _("Address"),
        blank=True
    )
    date_of_birth = models.DateField(
        _("Date of Birth"),
        null=True, blank=True
    )
    company_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    industry = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username

class Client(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='client_profile'
    )
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    registration_date = models.DateTimeField(
        _("Registration Date"),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __str__(self):
        return self.company_name

class ClientFile(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='files'
    )
    file = models.FileField(
        upload_to='client_files/'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )
    uploaded_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_files'
    )

    class Meta:
        verbose_name = _("Client File")
        verbose_name_plural = _("Client Files")

    def __str__(self):
        return f"{self.file.name} - {self.uploaded_at}"

class Laptop(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('retired', 'Retired'),
    ]
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='laptops',
        null=True,
        blank=True,
    )
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(
        max_length=100,
        unique=True
    )
    purchase_date = models.DateField()
    warranty_end_date = models.DateField()
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    class Meta:
        verbose_name = _("Laptop")
        verbose_name_plural = _("Laptops")

    def __str__(self):
        return f"{self.brand} {self.model} - {self.serial_number}"

