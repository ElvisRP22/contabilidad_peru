from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/core/', include('apps.core.urls')),
    path('api/contabilidad/', include('apps.contabilidad.urls')),
    path('api/facturacion/', include('apps.facturacion.urls')),
    path('api/inventario/', include('apps.inventario.urls')),
    path('api/nomina/', include('apps.nomina.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)