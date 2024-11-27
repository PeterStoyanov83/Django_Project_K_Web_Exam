from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    agreement_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ClientFile(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    file = models.FileField(upload_to='client_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name} - {self.file.name}"

class Laptop(models.Model):
    identifier = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.identifier

