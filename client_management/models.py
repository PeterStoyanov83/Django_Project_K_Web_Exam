from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    location = models.CharField(max_length=100, blank=True)
    agreement_status = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=True)
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.company_name}"

class ClientFile(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='client_files/')
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.client.user.username} - {self.file_name}"

class Laptop(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('maintenance', 'Under Maintenance'),
    ]

    identifier = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='laptops')
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    assigned_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.identifier} - {self.model}"

