from django.conf.urls import patterns, url
from desarrollo.views import desarrollo_view
from desarrollo.views import calcular_costo_view
from desarrollo.views import fases_proyecto_view
from desarrollo.views import crear_fase_view, modificar_fase_view, eliminar_fase_view, visualizar_fase_view, subir_fase_view, bajar_fase_view
from desarrollo.views import roles_fase_view, fase_agregar_rol_view, fase_confirmacion_agregar_rol_view, fase_quitar_rol_view
from desarrollo.views import tipos_item_fase_view
from desarrollo.views import crear_tipo_item_view, modificar_tipo_item_view, eliminar_tipo_item_view, visualizar_tipo_item_view
from desarrollo.views import tipos_atributo_tipo_item_view, agregar_tipo_atributo_view, confirmacion_agregar_tipo_atributo_view, quitar_tipo_atributo_view
from desarrollo.views import iniciar_fase_view
from desarrollo.views import finalizar_fase_view
from desarrollo.views import items_fase_view
from desarrollo.views import crear_item_view, modificar_item_view, eliminar_item_view, visualizar_item_view, aprobar_item_view, revivir_item_view, confirmacion_revivir_item_view
from desarrollo.views import relaciones_item_view, agregar_relacion_view, confirmacion_agregar_relacion_view, quitar_relacion_view
from desarrollo.views import versiones_item_view, confirmacion_reversionar_item_view

urlpatterns = patterns('',
    url(r'^desarrollo/$', desarrollo_view, name="vista_desarrollo"),
    url(r'^desarrollo/calcular_costo/proyecto/(?P<id_proyecto>\d+)/$', calcular_costo_view, name="vista_calcular_costo"),
    url(r'^desarrollo/fases/proyecto/(?P<id_proyecto>\d+)/$', fases_proyecto_view, name="vista_fases_proyecto"),
    url(r'^desarrollo/fases/crear_fase/proyecto/(?P<id_proyecto>\d+)/$', crear_fase_view, name="vista_crear_fase"),
    url(r'^desarrollo/fases/modificar_fase/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', modificar_fase_view, name="vista_modificar_fase"),
    url(r'^desarrollo/fases/eliminar_fase/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', eliminar_fase_view, name="vista_eliminar_fase"),
    url(r'^desarrollo/fases/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', visualizar_fase_view, name="vista_visualizar_fase"),
    url(r'^desarrollo/fases/subir_fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', subir_fase_view, name="vista_subir_fase"),
    url(r'^desarrollo/fases/bajar_fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', bajar_fase_view, name="vista_bajar_fase"),
    url(r'^desarrollo/fases/roles/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', roles_fase_view, name="vista_roles_fase"),
    url(r'^desarrollo/fases/agregar_rol/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', fase_agregar_rol_view, name="vista_fase_agregar_rol"),
    url(r'^desarrollo/fases/confirmacion_agregar_rol/(?P<id_rol>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', fase_confirmacion_agregar_rol_view, name="vista_confirmacion_fase_agregar_rol"),
    url(r'^desarrollo/fases/quitar_rol/(?P<id_rol>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', fase_quitar_rol_view, name="vista_fase_quitar_rol"),
    url(r'^desarrollo/fases/tipos_item/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', tipos_item_fase_view, name="vista_tipos_item_fase"),
    url(r'^desarrollo/fases/tipos_item/crear_tipo_item/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', crear_tipo_item_view, name="vista_crear_tipo_item"),  
    url(r'^desarrollo/fases/tipos_item/modificar_tipo_item/(?P<id_tipo_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', modificar_tipo_item_view, name="vista_modificar_tipo_item"),
    url(r'^desarrollo/fases/tipos_item/eliminar_tipo_item/(?P<id_tipo_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', eliminar_tipo_item_view, name="vista_eliminar_tipo_item"),
    url(r'^desarrollo/fases/tipos_item/tipo_item/(?P<id_tipo_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', visualizar_tipo_item_view, name="vista_visualizar_tipo_item"),
    url(r'^desarrollo/fases/tipos_item/tipos_atributo/tipo_item/(?P<id_tipo_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', tipos_atributo_tipo_item_view, name="vista_tipos_atributo_tipo_item"),
    url(r'^desarrollo/fases/tipos_item/agregar_tipo_atributo/tipo_item/(?P<id_tipo_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', agregar_tipo_atributo_view, name="vista_agregar_tipo_atributo"),
    url(r'^desarrollo/fases/tipos_item/confirmacion_agregar_tipo_atributo/(?P<id_tipo_atributo>\d+)/tipo_item/(?P<id_tipo_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', confirmacion_agregar_tipo_atributo_view, name="vista_confirmacion_agregar_tipo_atributo"),
    url(r'^desarrollo/fases/tipos_item/quitar_tipo_atributo/(?P<id_tipo_atributo>\d+)/tipo_item/(?P<id_tipo_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', quitar_tipo_atributo_view, name="vista_quitar_tipo_atributo"),
    url(r'^desarrollo/fases/iniciar_fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', iniciar_fase_view, name="vista_iniciar_fase"),
    url(r'^desarrollo/fases/items/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', items_fase_view, name="vista_items_fase"),
    url(r'^desarrollo/fases/items/crear_item/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', crear_item_view, name="vista_crear_item"),
    url(r'^desarrollo/fases/items/modificar_item/(?P<id_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', modificar_item_view, name="vista_modificar_item"),
    url(r'^desarrollo/fases/items/eliminar_item/(?P<id_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', eliminar_item_view, name="vista_eliminar_item"),
    url(r'^desarrollo/fases/items/item/(?P<id_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', visualizar_item_view, name="vista_visualizar_item"),
    url(r'^desarrollo/fases/items/aprobar_item/(?P<id_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', aprobar_item_view, name="vista_aprobar_item"),
    url(r'^desarrollo/fases/items/revivir_item/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', revivir_item_view, name="vista_revivir_item"),
    url(r'^desarrollo/fases/items/confirmacion_revivir_item/(?P<id_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', confirmacion_revivir_item_view, name="vista_confirmacion_revivir_item"),
    url(r'^desarrollo/fases/items/relaciones/item/(?P<id_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', relaciones_item_view, name="vista_relaciones_item"),
    url(r'^desarrollo/fases/items/agregar_relacion/item/(?P<id_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', agregar_relacion_view, name="vista_agregar_relacion"),
    url(r'^desarrollo/fases/items/confirmacion_agregar_relacion/(?P<id_relacion>\d+)/item/(?P<id_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', confirmacion_agregar_relacion_view, name="vista_confirmacion_agregar_relacion"),
    url(r'^desarrollo/fases/items/quitar_relacion/(?P<id_relacion>\d+)/item/(?P<id_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', quitar_relacion_view, name="vista_quitar_relacion"),
    url(r'^desarrollo/fases/items/versiones/item/(?P<id_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', versiones_item_view, name="vista_versiones_item"),
    url(r'^desarrollo/fases/items/confirmacion_reversionar_item/(?P<id_reversion>\d+)/item/(?P<id_item>\d+)/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', confirmacion_reversionar_item_view, name="vista_confirmacion_reversionar_item"),
    url(r'^desarrollo/fases/finalizar_fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', finalizar_fase_view, name="vista_finalizar_fase"),
)