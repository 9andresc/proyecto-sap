from django.conf.urls import patterns, include, url
from settings import MEDIA_ROOT
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('inicio.urls')),
    url(r'^', include('administracion.urls')),
    url(r'^', include('desarrollo.urls')),
    #url(r'^gestion_cambios/', include('gestion_cambios.urls')),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
)