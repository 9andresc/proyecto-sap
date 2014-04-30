from django.conf.urls import patterns, url
from desarrollo.views import desarrollo_view
from desarrollo.views import calcular_costo_view
from desarrollo.views import fases_proyecto_view
from desarrollo.views import items_fase_view
from desarrollo.views import crear_item_view, modificar_item_view, eliminar_item_view, visualizar_item_view

urlpatterns = patterns('',
    url(r'^desarrollo/$', desarrollo_view, name="vista_desarrollo"),
    url(r'^desarrollo/calcular_costo/proyecto/(?P<id_proyecto>.*)/$', calcular_costo_view, name="vista_desarrollo_calcular_costo"),
    url(r'^desarrollo/fases/proyecto/(?P<id_proyecto>.*)/$', fases_proyecto_view, name="vista_desarrollo_fases_proyecto"),
    url(r'^desarrollo/items/fase/(?P<id_fase>.*)/proyecto/(?P<id_proyecto>.*)/$', items_fase_view, name="vista_desarrollo_items_fase"),
    url(r'^desarrollo/items/crear_item/fase/(?P<id_fase>.*)/proyecto/(?P<id_proyecto>.*)/$', crear_item_view, name="vista_desarrollo_crear_item"),
    url(r'^desarrollo/items/modificar_item/(?P<id_item>.*)/fase/(?P<id_fase>.*)/proyecto/(?P<id_proyecto>.*)/$', modificar_item_view, name="vista_desarrollo_modificar_item"),
    url(r'^desarrollo/items/eliminar_item/(?P<id_item>.*)/fase/(?P<id_fase>.*)/proyecto/(?P<id_proyecto>.*)/$', eliminar_item_view, name="vista_desarrollo_eliminar_item"),
    url(r'^desarrollo/items/item/(?P<id_item>.*)/fase/(?P<id_fase>.*)/proyecto/(?P<id_proyecto>.*)/$', visualizar_item_view, name="vista_desarrollo_visualizar_item"),
)