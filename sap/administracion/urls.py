from django.conf.urls import patterns, url
# -------------- Vistas de usuarios -------------- #
from administracion.views import crear_usuario_view, gestion_usuarios_view, visualizar_usuario_view, modificar_usuario_view, cambiar_contrasenha_view, eliminar_usuario_view, roles_usuario_view, agregar_rol_view, confirmacion_agregar_rol_view, quitar_rol_view
# -------------- Vistas de roles -------------- #
from administracion.views import gestion_roles_view, crear_rol_view, visualizar_rol_view, modificar_rol_view, eliminar_rol_view, permisos_rol_view, agregar_permiso_view, confirmacion_agregar_permiso_view, quitar_permiso_view
# -------------- Vistas de tipos de atributo -------------- #
from administracion.views import gestion_tipos_atributo_view, crear_tipo_atributo_view, visualizar_tipo_atributo_view, modificar_tipo_atributo_view, eliminar_tipo_atributo_view
# -------------- Vistas de proyectos -------------- #
from administracion.views import gestion_proyectos_view, crear_proyecto_view, visualizar_proyecto_view, modificar_proyecto_view, eliminar_proyecto_view
from administracion.views import usuarios_proyecto_view, proyecto_agregar_usuario_view, confirmacion_proyecto_agregar_usuario_view, proyecto_quitar_usuario_view
from administracion.views import fases_proyecto_view, proyecto_agregar_fase_view, confirmacion_proyecto_agregar_fase_view, proyecto_quitar_fase_view
from administracion.views import roles_proyecto_view, proyecto_agregar_rol_view, confirmacion_proyecto_agregar_rol_view, proyecto_quitar_rol_view
from administracion.views import comite_proyecto_view, proyecto_agregar_miembro_view, confirmacion_proyecto_agregar_miembro_view, proyecto_quitar_miembro_view
from administracion.views import iniciar_proyecto_view
# -------------- Vistas de fases -------------- #
from administracion.views import gestion_fases_view, crear_fase_view, modificar_fase_view, eliminar_fase_view, visualizar_fase_view
from administracion.views import roles_fase_view, fase_agregar_rol_view, confirmacion_fase_agregar_rol_view, fase_quitar_rol_view
# -------------- Vistas de tipos de item -------------- #
from administracion.views import gestion_tipos_item_view

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
    url(r'^administracion/gestion_proyectos/crear_proyecto/$', crear_proyecto_view, name="vista_crear_proyecto"),
    url(r'^administracion/gestion_proyectos/proyecto/(?P<id_proyecto>.*)/$', visualizar_proyecto_view, name="vista_visualizar_proyecto"),
    url(r'^administracion/gestion_proyectos/modificar_proyecto/(?P<id_proyecto>.*)/$', modificar_proyecto_view, name="vista_modificar_proyecto"),
    url(r'^administracion/gestion_proyectos/eliminar_proyecto/(?P<id_proyecto>.*)/$', eliminar_proyecto_view, name="vista_eliminar_proyecto"),
    url(r'^administracion/gestion_proyectos/usuarios/proyecto/(?P<id_proyecto>.*)/$', usuarios_proyecto_view, name="vista_usuarios_proyecto"),
    url(r'^administracion/gestion_proyectos/agregar_usuario/proyecto/(?P<id_proyecto>.*)/$', proyecto_agregar_usuario_view, name="vista_proyecto_agregar_usuario"),
    url(r'^administracion/gestion_proyectos/confirmacion_agregar_usuario/proyecto/(?P<id_proyecto>.*)/(?P<id_usuario>.*)/$', confirmacion_proyecto_agregar_usuario_view, name="vista_confirmacion_proyecto_agregar_usuario"),
    url(r'^administracion/gestion_proyectos/quitar_usuario/proyecto/(?P<id_proyecto>.*)/(?P<id_usuario>.*)/$', proyecto_quitar_usuario_view, name="vista_proyecto_quitar_usuario"),
    url(r'^administracion/gestion_proyectos/fases/proyecto/(?P<id_proyecto>.*)/$', fases_proyecto_view, name="vista_fases_proyecto"),
    url(r'^administracion/gestion_proyectos/agregar_fase/proyecto/(?P<id_proyecto>.*)/$', proyecto_agregar_fase_view, name="vista_proyecto_agregar_fase"),
    url(r'^administracion/gestion_proyectos/confirmacion_agregar_fase/proyecto/(?P<id_proyecto>.*)/(?P<id_fase>.*)/$', confirmacion_proyecto_agregar_fase_view, name="vista_confirmacion_proyecto_agregar_fase"),
    url(r'^administracion/gestion_proyectos/quitar_fase/proyecto/(?P<id_proyecto>.*)/(?P<id_fase>.*)/$', proyecto_quitar_fase_view, name="vista_proyecto_quitar_fase"),
    url(r'^administracion/gestion_proyectos/roles/proyecto/(?P<id_proyecto>.*)/$', roles_proyecto_view, name="vista_roles_proyecto"),
    url(r'^administracion/gestion_proyectos/agregar_rol/proyecto/(?P<id_proyecto>.*)/$', proyecto_agregar_rol_view, name="vista_proyecto_agregar_rol"),
    url(r'^administracion/gestion_proyectos/confirmacion_agregar_rol/proyecto/(?P<id_proyecto>.*)/(?P<id_rol>.*)/$', confirmacion_proyecto_agregar_rol_view, name="vista_confirmacion_proyecto_agregar_rol"),
    url(r'^administracion/gestion_proyectos/quitar_rol/proyecto/(?P<id_proyecto>.*)/(?P<id_rol>.*)/$', proyecto_quitar_rol_view, name="vista_proyecto_quitar_rol"),
    url(r'^administracion/gestion_proyectos/comite/proyecto/(?P<id_proyecto>.*)/$', comite_proyecto_view, name="vista_comite_proyecto"),
    url(r'^administracion/gestion_proyectos/agregar_miembro_comite/proyecto/(?P<id_proyecto>.*)/$', proyecto_agregar_miembro_view, name="vista_proyecto_agregar_miembro"),
    url(r'^administracion/gestion_proyectos/confirmacion_agregar_miembro/proyecto/(?P<id_proyecto>.*)/(?P<id_usuario>.*)/$', confirmacion_proyecto_agregar_miembro_view, name="vista_confirmacion_proyecto_agregar_miembro"),
    url(r'^administracion/gestion_proyectos/quitar_miembro/proyecto/(?P<id_proyecto>.*)/(?P<id_usuario>.*)/$', proyecto_quitar_miembro_view, name="vista_proyecto_quitar_miembro"),
    url(r'^administracion/gestion_proyectos/iniciar_proyecto/(?P<id_proyecto>.*)/$', iniciar_proyecto_view, name="vista_iniciar_proyecto"),
    url(r'^administracion/gestion_fases/$', gestion_fases_view, name="vista_gestion_fases"),
    url(r'^administracion/gestion_fases/crear_fase/$', crear_fase_view, name="vista_crear_fase"),
    url(r'^administracion/gestion_fases/modificar_fase/(?P<id_fase>.*)/$', modificar_fase_view, name="vista_modificar_fase"),
    url(r'^administracion/gestion_fases/eliminar_fase/(?P<id_fase>.*)/$', eliminar_fase_view, name="vista_eliminar_fase"),
    url(r'^administracion/gestion_fases/fase/(?P<id_fase>.*)/$', visualizar_fase_view, name="vista_visualizar_fase"),
    url(r'^administracion/gestion_fases/roles/fase/(?P<id_fase>.*)/$', roles_fase_view, name="vista_roles_fase"),
    url(r'^administracion/gestion_fases/agregar_rol/fase/(?P<id_fase>.*)/$', fase_agregar_rol_view, name="vista_fase_agregar_rol"),
    url(r'^administracion/gestion_fases/confirmacion_agregar_rol/fase/(?P<id_fase>.*)/(?P<id_rol>.*)/$', confirmacion_fase_agregar_rol_view, name="vista_confirmacion_fase_agregar_rol"),
    url(r'^administracion/gestion_fases/quitar_rol/fase/(?P<id_fase>.*)/(?P<id_rol>.*)/$', fase_quitar_rol_view, name="vista_fase_quitar_rol"),
    url(r'^administracion/gestion_tipos_item/$', gestion_tipos_item_view, name="vista_gestion_tipos_item"),  
)
