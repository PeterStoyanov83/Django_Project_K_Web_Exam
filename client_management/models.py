from django.db import models
from django.contrib.auth.models import AbstractUser
import os

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.username

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=50)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.company_name}"

def client_file_path(instance, filename):
    return f'client_files/{instance.client.user.username}_{filename}'

class ClientFile(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=client_file_path)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.user.username} - {os.path.basename(self.file.name)}"

    @property
    def file_name(self):
        return os.path.basename(self.file.name)

    @property
    def file_type(self):
        return self.file_name.split('.')[-1] if '.' in self.file_name else ''

class Laptop(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Maintenance'),
        ('retired', 'Retired')
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='laptops')
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50, unique=True)
    purchase_date = models.DateField()
    warranty_end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.brand} {self.model} - {self.client.user.username}"

