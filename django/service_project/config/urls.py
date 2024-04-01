from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('link/', include('link_generator.urls')),
    path('api/', include('api.urls')),
    path('api/', include('phrase_json.urls')),
    path('', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)