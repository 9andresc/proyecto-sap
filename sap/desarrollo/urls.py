from django.conf.urls import patterns, url
from desarrollo.views import desarrollo_view
from desarrollo.views import fases_proyecto_view
from desarrollo.views import items_fase_view
from desarrollo.views import crear_item_view

urlpatterns = patterns('',
    url(r'^desarrollo/$', desarrollo_view, name="vista_desarrollo"),
    url(r'^desarrollo/fases/proyecto/(?P<id_proyecto>.*)/$', fases_proyecto_view, name="vista_desarrollo_fases_proyecto"),
    url(r'^desarrollo/items/fase/(?P<id_fase>.*)/proyecto/(?P<id_proyecto>.*)/$', items_fase_view, name="vista_desarrollo_items_fase"),
    url(r'^desarrollo/items/crear_item/fase/(?P<id_fase>.*)/proyecto/(?P<id_proyecto>.*)/$', crear_item_view, name="vista_desarrollo_crear_item"),
)