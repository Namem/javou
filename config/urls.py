# Em config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings               # Importe o settings
from django.conf.urls.static import static     # Importe o static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('dashboard.urls')), 
    path('chamados/', include('chamados.urls')),  
    path('kb/', include('knowledge_base.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
