from django.conf.urls import patterns, url
from administracion.views import crear_usuario_view, gestion_usuarios_view, visualizar_usuario_view, modificar_usuario_view, eliminar_usuario_view, roles_usuario_view, agregar_rol_view, confirmacion_agregar_rol_view, confirmacion_quitar_rol_view
from administracion.views import gestion_roles_view
urlpatterns = patterns('',
    url(r'^administracion/gestion_usuarios/$', gestion_usuarios_view, name="vista_gestion_usuarios"),
    url(r'^administracion/gestion_usuarios/crear_usuario/$', crear_usuario_view, name="vista_crear_usuario"),
    url(r'^administracion/gestion_usuarios/usuario/(?P<id_usuario>.*)/$', visualizar_usuario_view, name="vista_visualizar_usuario"),
    url(r'^administracion/gestion_usuarios/modificar_usuario/(?P<id_usuario>.*)/$', modificar_usuario_view, name="vista_modificar_usuario"),
    url(r'^administracion/gestion_usuarios/eliminar_usuario/(?P<id_usuario>.*)/$', eliminar_usuario_view, name="vista_eliminar_usuario"),
    url(r'^administracion/gestion_usuarios/roles/usuario/(?P<id_usuario>.*)/$', roles_usuario_view, name="vista_roles_usuario"),
    url(r'^administracion/gestion_usuarios/agregar_rol/usuario/(?P<id_usuario>.*)/$', agregar_rol_view, name="vista_agregar_rol"),
    url(r'^administracion/gestion_usuarios/confirmacion_agregar_rol/usuario/(?P<id_usuario>.*)/(?P<id_rol>.*)/$', confirmacion_agregar_rol_view, name="vista_confirmacion_agregar_rol"),
    url(r'^administracion/gestion_usuarios/confirmacion_quitar_rol/usuario/(?P<id_usuario>.*)/(?P<id_rol>.*)/$', confirmacion_quitar_rol_view, name="vista_quitar_agregar_rol"),
    url(r'^administracion/gestion_roles/$', gestion_roles_view, name="vista_gestion_roles"),
)