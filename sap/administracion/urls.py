from django.conf.urls import patterns, url
# -------------- Vistas de usuarios -------------- #
from administracion.views import gestion_usuarios_view
from administracion.views import crear_usuario_view, modificar_usuario_view, cambiar_contrasenha_view, eliminar_usuario_view, visualizar_usuario_view
from administracion.views import roles_usuario_view, usuario_agregar_rol_view, usuario_confirmacion_agregar_rol_view, usuario_quitar_rol_view
# -------------- Vistas de roles -------------- #
from administracion.views import gestion_roles_view
from administracion.views import crear_rol_view, visualizar_rol_view, modificar_rol_view, eliminar_rol_view
from administracion.views import permisos_rol_view, agregar_permiso_view, confirmacion_agregar_permiso_view, quitar_permiso_view
# -------------- Vistas de tipos de atributo -------------- #
from administracion.views import gestion_tipos_atributo_view
from administracion.views import crear_tipo_atributo_view, visualizar_tipo_atributo_view, modificar_tipo_atributo_view, eliminar_tipo_atributo_view
# -------------- Vistas de proyectos -------------- #
from administracion.views import gestion_proyectos_view
from administracion.views import crear_proyecto_view, visualizar_proyecto_view, modificar_proyecto_view, eliminar_proyecto_view
from administracion.views import usuarios_proyecto_view, proyecto_agregar_usuario_view, proyecto_confirmacion_agregar_usuario_view, proyecto_quitar_usuario_view
from administracion.views import roles_proyecto_view, proyecto_agregar_rol_view, proyecto_confirmacion_agregar_rol_view, proyecto_quitar_rol_view
from administracion.views import comite_proyecto_view, proyecto_agregar_miembro_view, proyecto_confirmacion_agregar_miembro_view, proyecto_quitar_miembro_view
from administracion.views import fases_proyecto_view, crear_fase_view, modificar_fase_view, eliminar_fase_view, visualizar_fase_view, subir_fase_view, bajar_fase_view
from administracion.views import iniciar_proyecto_view

urlpatterns = patterns('',
    url(r'^administracion/gestion_usuarios/$', gestion_usuarios_view, name="vista_gestion_usuarios"),
    url(r'^administracion/gestion_usuarios/crear_usuario/$', crear_usuario_view, name="vista_crear_usuario"),
    url(r'^administracion/gestion_usuarios/usuario/(?P<id_usuario>\d+)/$', visualizar_usuario_view, name="vista_visualizar_usuario"),
    url(r'^administracion/gestion_usuarios/modificar_usuario/(?P<id_usuario>\d+)/$', modificar_usuario_view, name="vista_modificar_usuario"),
    url(r'^administracion/gestion_usuarios/cambiar_contrasenha/(?P<id_usuario>\d+)/$', cambiar_contrasenha_view, name="vista_cambiar_contrasenha"),
    url(r'^administracion/gestion_usuarios/eliminar_usuario/(?P<id_usuario>\d+)/$', eliminar_usuario_view, name="vista_eliminar_usuario"),
    url(r'^administracion/gestion_usuarios/roles/usuario/(?P<id_usuario>\d+)/$', roles_usuario_view, name="vista_roles_usuario"),
    url(r'^administracion/gestion_usuarios/agregar_rol/usuario/(?P<id_usuario>\d+)/$', usuario_agregar_rol_view, name="vista_usuario_agregar_rol"),
    url(r'^administracion/gestion_usuarios/confirmacion_agregar_rol/(?P<id_rol>\d+)/usuario/(?P<id_usuario>\d+)/$', usuario_confirmacion_agregar_rol_view, name="vista_usuario_confirmacion_agregar_rol"),
    url(r'^administracion/gestion_usuarios/quitar_rol/(?P<id_rol>\d+)/usuario/(?P<id_usuario>\d+)/$', usuario_quitar_rol_view, name="vista_usuario_quitar_rol"),
    url(r'^administracion/gestion_roles/$', gestion_roles_view, name="vista_gestion_roles"),
    url(r'^administracion/gestion_roles/crear_rol/$', crear_rol_view, name="vista_crear_rol"),
    url(r'^administracion/gestion_roles/rol/(?P<id_rol>\d+)/$', visualizar_rol_view, name="vista_visualizar_rol"),
    url(r'^administracion/gestion_roles/modificar_rol/(?P<id_rol>\d+)/$', modificar_rol_view, name="vista_modificar_rol"),
    url(r'^administracion/gestion_roles/eliminar_rol/(?P<id_rol>\d+)/$', eliminar_rol_view, name="vista_eliminar_rol"),
    url(r'^administracion/gestion_roles/permisos/rol/(?P<id_rol>\d+)/$', permisos_rol_view, name="vista_permisos_rol"),
    url(r'^administracion/gestion_roles/agregar_permiso/rol/(?P<id_rol>\d+)/$', agregar_permiso_view, name="vista_agregar_permiso"),
    url(r'^administracion/gestion_roles/confirmacion_agregar_permiso/(?P<id_permiso>\d+)/rol/(?P<id_rol>\d+)/$', confirmacion_agregar_permiso_view, name="vista_confirmacion_agregar_permiso"),
    url(r'^administracion/gestion_roles/quitar_permiso/(?P<id_permiso>\d+)/rol/(?P<id_rol>\d+)/$', quitar_permiso_view, name="vista_quitar_permiso"),
    url(r'^administracion/gestion_tipos_atributo/$', gestion_tipos_atributo_view, name="vista_gestion_tipos_atributo"),
    url(r'^administracion/gestion_tipos_atributo/crear_tipo_atributo/$', crear_tipo_atributo_view, name="vista_crear_tipo_atributo"),
    url(r'^administracion/gestion_tipos_atributo/tipo_atributo/(?P<id_tipo_atributo>\d+)/$', visualizar_tipo_atributo_view, name="vista_visualizar_tipo_atributo"),
    url(r'^administracion/gestion_tipos_atributo/modificar_tipo_atributo/(?P<id_tipo_atributo>\d+)/$', modificar_tipo_atributo_view, name="vista_modificar_tipo_atributo"),
    url(r'^administracion/gestion_tipos_atributo/eliminar_tipo_atributo/(?P<id_tipo_atributo>\d+)/$', eliminar_tipo_atributo_view, name="vista_eliminar_tipo_atributo"),
    url(r'^administracion/gestion_proyectos/$', gestion_proyectos_view, name="vista_gestion_proyectos"),
    url(r'^administracion/gestion_proyectos/crear_proyecto/$', crear_proyecto_view, name="vista_crear_proyecto"),
    url(r'^administracion/gestion_proyectos/proyecto/(?P<id_proyecto>\d+)/$', visualizar_proyecto_view, name="vista_visualizar_proyecto"),
    url(r'^administracion/gestion_proyectos/modificar_proyecto/(?P<id_proyecto>\d+)/$', modificar_proyecto_view, name="vista_modificar_proyecto"),
    url(r'^administracion/gestion_proyectos/eliminar_proyecto/(?P<id_proyecto>\d+)/$', eliminar_proyecto_view, name="vista_eliminar_proyecto"),
    url(r'^administracion/gestion_proyectos/usuarios/proyecto/(?P<id_proyecto>\d+)/$', usuarios_proyecto_view, name="vista_usuarios_proyecto"),
    url(r'^administracion/gestion_proyectos/agregar_usuario/proyecto/(?P<id_proyecto>\d+)/$', proyecto_agregar_usuario_view, name="vista_proyecto_agregar_usuario"),
    url(r'^administracion/gestion_proyectos/confirmacion_agregar_usuario/(?P<id_usuario>\d+)/proyecto/(?P<id_proyecto>\d+)/$', proyecto_confirmacion_agregar_usuario_view, name="vista_proyecto_confirmacion_agregar_usuario"),
    url(r'^administracion/gestion_proyectos/quitar_usuario/(?P<id_usuario>\d+)/proyecto/(?P<id_proyecto>\d+)/$', proyecto_quitar_usuario_view, name="vista_proyecto_quitar_usuario"),
    url(r'^administracion/gestion_proyectos/roles/proyecto/(?P<id_proyecto>\d+)/$', roles_proyecto_view, name="vista_roles_proyecto"),
    url(r'^administracion/gestion_proyectos/agregar_rol/proyecto/(?P<id_proyecto>\d+)/$', proyecto_agregar_rol_view, name="vista_proyecto_agregar_rol"),
    url(r'^administracion/gestion_proyectos/confirmacion_agregar_rol/(?P<id_rol>\d+)/proyecto/(?P<id_proyecto>\d+)/$', proyecto_confirmacion_agregar_rol_view, name="vista_proyecto_confirmacion_agregar_rol"),
    url(r'^administracion/gestion_proyectos/quitar_rol/(?P<id_rol>\d+)/proyecto/(?P<id_proyecto>\d+)/$', proyecto_quitar_rol_view, name="vista_proyecto_quitar_rol"),
    url(r'^administracion/gestion_proyectos/comite/proyecto/(?P<id_proyecto>\d+)/$', comite_proyecto_view, name="vista_comite_proyecto"),
    url(r'^administracion/gestion_proyectos/agregar_miembro_comite/proyecto/(?P<id_proyecto>\d+)/$', proyecto_agregar_miembro_view, name="vista_proyecto_agregar_miembro"),
    url(r'^administracion/gestion_proyectos/confirmacion_agregar_miembro/(?P<id_usuario>\d+)/proyecto/(?P<id_proyecto>\d+)/$', proyecto_confirmacion_agregar_miembro_view, name="vista_proyecto_confirmacion_agregar_miembro"),
    url(r'^administracion/gestion_proyectos/quitar_miembro/(?P<id_usuario>\d+)/proyecto/(?P<id_proyecto>\d+)/$', proyecto_quitar_miembro_view, name="vista_proyecto_quitar_miembro"),
    url(r'^administracion/gestion_proyectos/fases/proyecto/(?P<id_proyecto>\d+)/$', fases_proyecto_view, name="vista_fases_proyecto"),
    url(r'^administracion/gestion_proyectos/fases/crear_fase/proyecto/(?P<id_proyecto>\d+)/$', crear_fase_view, name="vista_crear_fase"),
    url(r'^administracion/gestion_proyectos/fases/modificar_fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', modificar_fase_view, name="vista_modificar_fase"),
    url(r'^administracion/gestion_proyectos/fases/eliminar_fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', eliminar_fase_view, name="vista_eliminar_fase"),
    url(r'^administracion/gestion_proyectos/fases/fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', visualizar_fase_view, name="vista_visualizar_fase"),
    url(r'^administracion/gestion_proyectos/fases/subir_fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', subir_fase_view, name="vista_subir_fase"),
    url(r'^administracion/gestion_proyectos/fases/bajar_fase/(?P<id_fase>\d+)/proyecto/(?P<id_proyecto>\d+)/$', bajar_fase_view, name="vista_bajar_fase"),
    url(r'^administracion/gestion_proyectos/iniciar_proyecto/(?P<id_proyecto>\d+)/$', iniciar_proyecto_view, name="vista_iniciar_proyecto"),   
)