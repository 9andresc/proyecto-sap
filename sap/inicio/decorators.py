from django.template import RequestContext
from django.shortcuts import render_to_response
from functools import wraps
from administracion.models import Rol, Permiso, Proyecto
from desarrollo.models import SolicitudCambio

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
            es_miembro = False
            proyecto = Proyecto.objects.get(id=id_proyecto)
            for u in proyecto.usuarios.all():
                if request.user.id == u.id:
                    es_miembro = True
                    break
            if es_miembro:
                return func(request, id_proyecto, *args, **kwargs)
            for u in proyecto.comite_de_cambios.all():
                if request.user.id == u.id:
                    es_miembro = True
                    break
            if es_miembro:
                return func(request, id_proyecto, *args, **kwargs)
            ctx = {'es_miembro':es_miembro}
            return render_to_response("acceso_denegado.html", ctx, context_instance=RequestContext(request))
        return wraps(func)(inner_decorator)
    return decorator

def miembro_comite():
    def decorator(func):
        def inner_decorator(request, id_proyecto, *args, **kwargs):
            es_miembro_comite = False
            proyecto = Proyecto.objects.get(id=id_proyecto)
            for u in proyecto.comite_de_cambios.all():
                if request.user.id == u.id:
                    es_miembro_comite = True
                    break
            if es_miembro_comite:
                return func(request, id_proyecto, *args, **kwargs)
            ctx = {'es_miembro_comite':es_miembro_comite}
            return render_to_response("acceso_denegado.html", ctx, context_instance=RequestContext(request))
        return wraps(func)(inner_decorator)
    return decorator

def solicitud_requerida(accion):
    def decorator(func):
        def inner_decorator(request, id_proyecto, id_fase, id_item, *args, **kwargs):
            proyecto = Proyecto.objects.get(id=id_proyecto)
            fase = proyecto.fases.get(id=id_fase)
            item = fase.items.get(id=id_item)
            solicitudes_item = SolicitudCambio.objects.filter(item=item)
            
            if item.estado != 2 and solicitudes_item:
                try:
                    solicitud = solicitudes_item.get(accion=accion)
                except SolicitudCambio.DoesNotExist:
                    estado_bloqueado = False
                    existe_solicitud = False
                    ctx = {'item':item, 'existe_solicitud':existe_solicitud, 'estado_bloqueado':estado_bloqueado}
                    return render_to_response("acceso_denegado.html", ctx, context_instance=RequestContext(request))
            
            # Verificamos si el item a modificar esta en un estado distinto a Bloqueado.
            if item.estado != 2:
                return func(request, id_proyecto, id_fase, id_item, *args, **kwargs)
            # Si no esta Bloqueado, se buscaran solicitudes del item a modificar.
            else:
                proyecto = fase.proyecto
                linea_base = item.linea_base
                existe_solicitud = False
                solicitudes = SolicitudCambio.objects.filter(item=item)
                # Verificamos si existen solicitudes del item a modificar.
                if solicitudes:
                    existe_solicitud = True
                    
                if existe_solicitud:
                    try:
                        # Verificamos si entre las solicitudes del item existe una que concuerde con la accion a realizar sobre el item.
                        solicitud = solicitudes.get(accion=accion)
                    except SolicitudCambio.DoesNotExist:
                        existe_solicitud = False
                        
                    if existe_solicitud:
                        # Verificamos si la solicitud encontrada esta aprobada o no
                        if solicitud.aprobada == True:
                            # Si esta aprobada, entonces, se continua con la accion a realizar sobre el item.
                            return func(request, id_proyecto, id_fase, id_item, *args, **kwargs)
                        # Si no esta aprobada, entonces, se envia una notificacion al usuario de que su solicitud se encuentra en tramite.
                        elif solicitud.aprobada == False:
                            solicitud_aprobada = False
                            ctx = {'item':item, 'linea_base':linea_base, 'fase':fase, 'proyecto':proyecto, 'solicitud_aprobada':solicitud_aprobada, 'existe_solicitud':existe_solicitud}
                            return render_to_response("acceso_denegado.html", ctx, context_instance=RequestContext(request))
                        else:
                            ctx = {'item':item, 'existe_solicitud':existe_solicitud}
                            return render_to_response("acceso_denegado.html", ctx, context_instance=RequestContext(request))
                    # Si no existe una solicitud de cambio para esta accion sobre el item, entonces, se envia una notificacion al usuario 
                    # de que no existe una solicitud de cambio.
                    else:
                        ctx = {'item':item, 'linea_base':linea_base, 'fase':fase, 'proyecto':proyecto, 'existe_solicitud':existe_solicitud}
                        return render_to_response("acceso_denegado.html", ctx, context_instance=RequestContext(request))
                # Si no existe una solicitud de cambio para el item, entonces, se envia una notificacion al usuario de que no existe
                # una solicitud de cambio.
                else:
                    ctx = {'item':item, 'linea_base':linea_base, 'fase':fase, 'proyecto':proyecto, 'existe_solicitud':existe_solicitud}
                    return render_to_response("acceso_denegado.html", ctx, context_instance=RequestContext(request))
        return wraps(func)(inner_decorator)
    return decorator