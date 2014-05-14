from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('inicio.urls')),
    url(r'^', include('administracion.urls')),
    url(r'^', include('desarrollo.urls')),
    #url(r'^gestion_cambios/', include('gestion_cambios.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)