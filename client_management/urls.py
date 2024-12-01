from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'client_management'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('laptops/', views.laptop_list, name='laptop_list'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='client_management/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='client_management/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='client_management/password_reset_complete.html'), name='password_reset_complete'),
    path('laptops/create/', views.laptop_create, name='laptop_create'),
    path('laptops/<int:pk>/update/', views.laptop_update, name='laptop_update'),
    path('laptops/<int:pk>/delete/', views.laptop_delete, name='laptop_delete'),
]

