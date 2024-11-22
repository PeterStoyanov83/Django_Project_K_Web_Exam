from django.urls import path
from . import views

app_name = 'client_management'

urlpatterns = [
    path('', views.client_list, name='client_list'),
    path('client/<int:client_id>/', views.client_detail, name='client_detail'),
    path('client/<int:client_id>/edit/', views.client_edit, name='client_edit'),
    path('client/<int:client_id>/delete/', views.client_delete, name='client_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('laptops/', views.laptop_list, name='laptop_list'),
    path('laptop/<int:laptop_id>/', views.laptop_detail, name='laptop_detail'),
    path('laptop/<int:laptop_id>/edit/', views.laptop_edit, name='laptop_edit'),
    path('laptop/<int:laptop_id>/delete/', views.laptop_delete, name='laptop_delete'),
    path('client/<int:client_id>/upload/', views.client_file_upload, name='client_file_upload'),
]

