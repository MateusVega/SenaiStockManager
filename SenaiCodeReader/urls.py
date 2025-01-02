from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('reader.urls')),
    path('auth/', include('login.urls')),
    path('admin/', admin.site.urls),
]
