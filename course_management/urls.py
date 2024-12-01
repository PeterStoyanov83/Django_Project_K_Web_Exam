from django.urls import path
from . import views

app_name = 'course_management'

urlpatterns = [
    path('courses', views.course_list, name='course_list'),
    path('create/', views.course_create, name='course_create'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/update/', views.course_update, name='course_update'),
    path('<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('<int:course_pk>/schedule/create/', views.schedule_create, name='schedule_create'),
    path('schedules/<int:pk>/update/', views.schedule_update, name='schedule_update'),
    path('schedules/<int:pk>/delete/', views.schedule_delete, name='schedule_delete'),
    path('bookings/create/', views.booking_create, name='booking_create'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/cancel/', views.booking_cancel, name='booking_cancel'),
]
