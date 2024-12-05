from django.urls import path
from . import views

app_name = 'course_management'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('schedule/', views.schedule, name='schedule'),
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
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-course-applications/', views.admin_course_applications, name='admin_course_applications'),
    path('approve-application/<int:application_id>/', views.approve_course_application,
         name='approve_course_application'),
    path('reject-application/<int:application_id>/', views.reject_course_application, name='reject_course_application'),
    path('<int:course_id>/apply/', views.apply_for_course, name='apply_for_course'),
    path('admin-only/', views.admin_only_view, name='admin_only'),
    path('admin/courses/', views.admin_courses, name='admin_courses'),
    path('admin/lecturers/', views.admin_lecturers, name='admin_lecturers'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/lecturers/create/', views.lecturer_create, name='lecturer_create'),
    path('admin/lecturers/<int:pk>/edit/', views.lecturer_edit, name='lecturer_edit'),
    path('admin/users/create/', views.user_create, name='user_create'),
    path('admin/users/<int:pk>/edit/', views.user_edit, name='user_edit'),
]

