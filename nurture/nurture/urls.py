
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminapp/',include('adminapp.urls')),
    path('',include('users.urls')),
    path('products/',include('products.urls')),
]





urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
handler404 = 'products.views.handler404'
