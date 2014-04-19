from administracion.models import Rol, Permiso
from django.http.response import HttpResponseRedirect
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
            return HttpResponseRedirect('/acceso_denegado/')
        return wraps(func)(inner_decorator)
    return decorator