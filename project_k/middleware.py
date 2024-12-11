from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 302 and not request.user.is_authenticated:
            redirect_url = response.url
            if any(url in redirect_url for url in ['/profile/', '/course/', '/admin/']):
                messages.error(request, "Not allowed! Please log in first.")
                return render(request, '403.html', status=403)

        return response
