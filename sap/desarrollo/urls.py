from django.conf.urls import patterns, url
from desarrollo.views import desarrollo_view
from desarrollo.views import fases_proyecto_view

urlpatterns = patterns('',
    url(r'^desarrollo/$', desarrollo_view, name="vista_desarrollo"),
    url(r'^desarrollo/fases/proyecto/(?P<id_proyecto>.*)/$', fases_proyecto_view, name="vista_desarrollo_fases_proyecto"),
)