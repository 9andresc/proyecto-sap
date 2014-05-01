from administracion.models import Rol, Permiso, Proyecto, Fase
from django.template import RequestContext
from django.shortcuts import render_to_response
from functools import wraps

def permiso_requerido(permiso):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            roles = Rol.objects.filter(user__id=request.user.id)
            for rol in roles:
                permisos = Permiso.objects.filter(rol__id=rol.id)
                for perm in permisos:
                    if perm.nombre == permiso:
                        return func(request, *args, **kwargs)
            ctx = {'permiso':permiso}
            return render_to_response("acceso_denegado.html", ctx, context_instance=RequestContext(request))
        return wraps(func)(inner_decorator)
    return decorator

def miembro_proyecto():
    def decorator(func):
        def inner_decorator(request, id_proyecto, *args, **kwargs):
            proyecto = Proyecto.objects.get(id=id_proyecto)
            for u in proyecto.usuarios.all():
                if request.user.id == u.id:
                    return func(request, id_proyecto, *args, **kwargs)
            no_es_miembro = True
            ctx = {'no_es_miembro':no_es_miembro}
            return render_to_response("acceso_denegado.html", ctx, context_instance=RequestContext(request))
        return wraps(func)(inner_decorator)
    return decorator

def fase_miembro_proyecto():
    def decorator(func):
        def inner_decorator(request, id_fase, *args, **kwargs):
            fase = Fase.objects.get(id=id_fase)
            if fase.proyecto or fase.proyecto != None:
                proyecto = Proyecto.objects.get(id=fase.proyecto.id)
                for u in proyecto.usuarios.all():
                    if request.user.id == u.id:
                        return func(request, id_fase, *args, **kwargs)
            fase_no_es_miembro = True
            ctx = {'fase_no_es_miembro':fase_no_es_miembro}
            return render_to_response("acceso_denegado.html", ctx, context_instance=RequestContext(request))
        return wraps(func)(inner_decorator)
    return decorator