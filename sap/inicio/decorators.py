from administracion.models import Rol, Permiso
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