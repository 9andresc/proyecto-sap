from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^inicio/', include('inicio.urls')),
    #url(r'^admnistracion/', include('administracion.urls')),
    #url(r'^desarrollo/', include('desarrollo.urls')),
    #url(r'^gestion_cambios/', include('gestion_cambios.urls')),
)
