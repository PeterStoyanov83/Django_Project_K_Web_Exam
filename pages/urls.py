from django.urls import path
from . import views
from .views import healthz

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('healthz', healthz),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('restricted/', views.restricted_view, name='restricted_view'),

]
