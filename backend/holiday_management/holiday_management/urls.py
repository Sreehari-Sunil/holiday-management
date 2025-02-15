
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings as SETTINGS
from django.conf.urls.static import static
from django.views.static import serve
from holidays import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/holidays/', include('api.v1.holidays.urls', namespace="api_v1_holidays")),
    # Media & Static
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': SETTINGS.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': SETTINGS.STATIC_ROOT}),
]+ static(SETTINGS.MEDIA_URL, document_root=SETTINGS.MEDIA_ROOT)
