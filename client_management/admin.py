from django.contrib import admin
from .models import Client, ClientFile, Laptop

admin.site.register(Client)
admin.site.register(ClientFile)
admin.site.register(Laptop)

