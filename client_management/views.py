from django.shortcuts import render
from .models import Client

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_management/client_list.html', {'clients': clients})

