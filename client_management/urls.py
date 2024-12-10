from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'client_management'

urlpatterns = [
    path('profile/', login_required(views.profile), name='profile'),
    path('profile/edit/', login_required(views.profile_edit), name='profile_edit'),
    path('profile/upload-file/', views.upload_file, name='upload_file'),
    path('profile/delete-file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('my-schedule/', login_required(views.my_schedule), name='my_schedule'),
    path('laptops/', views.laptop_list, name='laptop_list'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='client_management/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='client_management/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='client_management/password_reset_complete.html'),
         name='password_reset_complete'),
    path('laptops/create/', views.laptop_create, name='laptop_create'),
    path('laptops/<int:pk>/update/', views.laptop_update, name='laptop_update'),
    path('laptops/<int:pk>/delete/', views.laptop_delete, name='laptop_delete'),

]
