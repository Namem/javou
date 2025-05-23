from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout
    path('', include('dashboard.urls')), 
    path('chamados/', include('chamados.urls')),  
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),  
]
