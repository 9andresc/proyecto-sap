from django.conf.urls import patterns, url
from administracion.views import crear_usuario_view, gestion_usuarios_view, visualizar_usuario_view, modificar_usuario_view, cambiar_contrasenha_view, eliminar_usuario_view, roles_usuario_view, agregar_rol_view, confirmacion_agregar_rol_view, quitar_rol_view
from administracion.views import gestion_roles_view, crear_rol_view, visualizar_rol_view, modificar_rol_view, eliminar_rol_view, permisos_rol_view, agregar_permiso_view, confirmacion_agregar_permiso_view, quitar_permiso_view
from administracion.views import gestion_tipos_atributo_view, crear_tipo_atributo_view, visualizar_tipo_atributo_view, modificar_tipo_atributo_view, eliminar_tipo_atributo_view
from administracion.views import gestion_proyectos_view
urlpatterns = patterns('',
    url(r'^administracion/gestion_usuarios/$', gestion_usuarios_view, name="vista_gestion_usuarios"),
    url(r'^administracion/gestion_usuarios/crear_usuario/$', crear_usuario_view, name="vista_crear_usuario"),
    url(r'^administracion/gestion_usuarios/usuario/(?P<id_usuario>.*)/$', visualizar_usuario_view, name="vista_visualizar_usuario"),
    url(r'^administracion/gestion_usuarios/modificar_usuario/(?P<id_usuario>.*)/$', modificar_usuario_view, name="vista_modificar_usuario"),
    url(r'^administracion/gestion_usuarios/cambiar_contrasenha/(?P<id_usuario>.*)/$', cambiar_contrasenha_view, name="vista_cambiar_contrasenha"),
    url(r'^administracion/gestion_usuarios/eliminar_usuario/(?P<id_usuario>.*)/$', eliminar_usuario_view, name="vista_eliminar_usuario"),
    url(r'^administracion/gestion_usuarios/roles/usuario/(?P<id_usuario>.*)/$', roles_usuario_view, name="vista_roles_usuario"),
    url(r'^administracion/gestion_usuarios/agregar_rol/usuario/(?P<id_usuario>.*)/$', agregar_rol_view, name="vista_agregar_rol"),
    url(r'^administracion/gestion_usuarios/confirmacion_agregar_rol/usuario/(?P<id_usuario>.*)/(?P<id_rol>.*)/$', confirmacion_agregar_rol_view, name="vista_confirmacion_agregar_rol"),
    url(r'^administracion/gestion_usuarios/quitar_rol/usuario/(?P<id_usuario>.*)/(?P<id_rol>.*)/$', quitar_rol_view, name="vista_quitar_rol"),
    url(r'^administracion/gestion_roles/$', gestion_roles_view, name="vista_gestion_roles"),
    url(r'^administracion/gestion_roles/crear_rol/$', crear_rol_view, name="vista_crear_rol"),
    url(r'^administracion/gestion_roles/rol/(?P<id_rol>.*)/$', visualizar_rol_view, name="vista_visualizar_rol"),
    url(r'^administracion/gestion_roles/modificar_rol/(?P<id_rol>.*)/$', modificar_rol_view, name="vista_modificar_rol"),
    url(r'^administracion/gestion_roles/eliminar_rol/(?P<id_rol>.*)/$', eliminar_rol_view, name="vista_eliminar_rol"),
    url(r'^administracion/gestion_roles/permisos/rol/(?P<id_rol>.*)/$', permisos_rol_view, name="vista_permisos_rol"),
    url(r'^administracion/gestion_roles/agregar_permiso/rol/(?P<id_rol>.*)/$', agregar_permiso_view, name="vista_agregar_permiso"),
    url(r'^administracion/gestion_roles/confirmacion_agregar_permiso/rol/(?P<id_rol>.*)/(?P<id_permiso>.*)/$', confirmacion_agregar_permiso_view, name="vista_confirmacion_agregar_permiso"),
    url(r'^administracion/gestion_roles/quitar_permiso/rol/(?P<id_rol>.*)/(?P<id_permiso>.*)/$', quitar_permiso_view, name="vista_quitar_agregar_permiso"),
    url(r'^administracion/gestion_tipos_atributo/$', gestion_tipos_atributo_view, name="vista_gestion_tipos_atributo"),
    url(r'^administracion/gestion_tipos_atributo/crear_tipo_atributo/$', crear_tipo_atributo_view, name="vista_crear_tipo_atributo"),
    url(r'^administracion/gestion_tipos_atributo/tipo_atributo/(?P<id_tipo_atributo>.*)/$', visualizar_tipo_atributo_view, name="vista_visualizar_tipo_atributo"),
    url(r'^administracion/gestion_tipos_atributo/modificar_tipo_atributo/(?P<id_tipo_atributo>.*)/$', modificar_tipo_atributo_view, name="vista_modificar_tipo_atributo"),
    url(r'^administracion/gestion_tipos_atributo/eliminar_tipo_atributo/(?P<id_tipo_atributo>.*)/$', eliminar_tipo_atributo_view, name="vista_eliminar_tipo_atributo"),
    url(r'^administracion/gestion_proyectos/$', gestion_proyectos_view, name="vista_gestion_proyectos"),
   
)
