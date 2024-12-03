from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from api.openai_assistant import chat_with_assistant

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('pages.urls')),
                  path('client/', include('client_management.urls')),
                  path('course/', include('course_management.urls', namespace='course_management')),
                  path('api/chat/', chat_with_assistant, name='chat_with_assistant'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
