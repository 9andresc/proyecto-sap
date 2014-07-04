import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template.loader import render_to_string
from django.http import HttpResponse
import datetime
import pydot
from django.conf import settings
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from administracion.models import Proyecto, Rol, TipoAtributo
from desarrollo.models import Item, Fase, TipoItem, ValorAtributo, VersionItem, LineaBase, SolicitudCambio
from desarrollo.forms import CrearItemForm, ModificarItemForm, CrearTipoItemForm, ModificarTipoItemForm, CrearLineaBaseForm, CrearSolicitudForm
from inicio.decorators import permiso_requerido, miembro_proyecto, rol_fase_requerido, miembro_comite, solicitud_requerida

@login_required(login_url='/login/')
def desarrollo_view(request):
    """
    ::
    
        La vista del modulo de desarrollo. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
                - El usuario debe estar logueado.
                
        Esta vista permite al usuario listar y conocer las opciones de los proyectos puestos en marcha.
        Inicialmente, se verifican los permisos del usuario solicitante para restringir (si es necesario) 
        los botones de accion sobre cada proyecto.
          
        La vista recibe los siguientes parametros:
    
                - request: contiene informacion sobre la sesion actual.
            
        La vista retorna lo siguiente:
      
                - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    calcular_costo = False
    gestionar_fases = False
    gestionar_solicitudes_proyecto = False
    gestionar_solicitudes_usuario = False
    finalizar_proyecto = False
    
    roles = request.user.roles.all()
    for r in roles:
        for p in r.permisos.all():
            if p.nombre == 'Calcular costo de proyecto':
                calcular_costo = True
            elif p.nombre == 'Gestionar fases de proyecto':
                gestionar_fases = True
            elif p.nombre == 'Gestionar solicitudes de proyecto':
                gestionar_solicitudes_proyecto = True
            elif p.nombre == 'Gestionar solicitudes de usuario':
                gestionar_solicitudes_usuario = True
            elif p.nombre == 'Finalizar proyecto':
                finalizar_proyecto = True
                
            if calcular_costo and gestionar_fases and gestionar_solicitudes_proyecto and gestionar_solicitudes_usuario and finalizar_proyecto:
                break
        if calcular_costo and gestionar_fases and gestionar_solicitudes_proyecto and gestionar_solicitudes_usuario and finalizar_proyecto:
                break
            
    proyectos = Proyecto.objects.filter(estado=1)
    finalizados = Proyecto.objects.filter(estado=2)
    ctx = {'proyectos': proyectos, 'finalizados':finalizados, 'calcular_costo':calcular_costo, 'gestionar_fases':gestionar_fases, 'gestionar_solicitudes_proyecto':gestionar_solicitudes_proyecto, 'gestionar_solicitudes_usuario':gestionar_solicitudes_usuario, 'finalizar_proyecto':finalizar_proyecto}
    return render_to_response('desarrollo/desarrollo.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Calcular costo de proyecto")
@miembro_proyecto()
def calcular_costo_view(request, id_proyecto):
    """
    ::
    
        La vista del calculo del costo total de un proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Calcular costo de proyecto.
            - Debe ser miembro del proyecto en cuestion.
            
        Esta vista permite al usuario conocer el costo total del proyecto seleccionado, para lograr esto, se recorren 
        todas las fases y todos los items, y se suman los costos individuales de cada item hasta terminar el ciclo de 
        recorrido por las fases del proyecto.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
    
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fases = proyecto.fases.all()
    fases_valido = False
    items_valido = False
    costo_total = 0
    if fases:
        fases_valido = True
        for f in fases:
            items = f.items.all()
            if items:
                items_valido = True
                for i in items:
                    costo_total = costo_total + i.costo_monetario
    ctx = {'proyecto':proyecto, 'fases_valido':fases_valido, 'items_valido':items_valido, 'costo_total':costo_total}
    return render_to_response('desarrollo/costo_total.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Finalizar proyecto")
@miembro_proyecto()
def finalizar_proyecto_view(request, id_proyecto):
    """
    ::
    
        La vista de finalizacion de un proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Finalizar proyecto.
            - Debe ser miembro del proyecto en cuestion.
            
        Esta vista permite a un usuario lider de un proyecto, finalizarlo. Para poder finalizar un proyecto se deben cumplir 
        las siguientes condiciones:
        
            - El proyecto se encuentra en estado En curso.
            - Todas las fases del proyecto se encuentran en estado Finalizado.
            - Todos los items de las fases del proyecto se encuentran en estado Bloqueado.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
    
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fases = proyecto.fases.all()
    estado_valido = True
    fases_finalizadas = True
    items_bloqueados = True
    
    if proyecto.estado != 1:
        estado_valido = False
    
    for f in fases:
        if f.estado != 2:
            fases_finalizadas = False
            break
        
    for f in fases:
        items = f.items.all()
        for i in items:
            if i.estado != 2:
                items_bloqueados = False
                break
        if items_bloqueados == False:
            break
        
    if estado_valido and fases_finalizadas and items_bloqueados:
        proyecto.estado = 2
        proyecto.save()
        
    ctx = {'proyecto':proyecto, 'estado_valido':estado_valido, 'items_bloqueados':items_bloqueados, 'fases_finalizadas':fases_finalizadas}
    return render_to_response('desarrollo/finalizar_proyecto.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar solicitudes de proyecto")
@miembro_proyecto()
@miembro_comite()
def solicitudes_proyecto_view(request, id_proyecto):
    """
    ::
    
        La vista de gestion de solicitudes de cambio. Se deben cumplir los siguientes requisitos para utilizar esta vista:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Gestionar solicitudes.
            - Debe ser miembro del proyecto en cuestion.
            
        Esta vista permite al usuario (miembro del comite de cambios) gestionar todas las solicitudes de cambio del proyecto. 
        Se cargan todas las solicitudes del proyecto y se envian como un listado al template de gestion de solicitudes
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
    
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    solicitudes = SolicitudCambio.objects.filter(proyecto=proyecto)
    ctx = {'proyecto':proyecto, 'solicitudes':solicitudes}
    return render_to_response('desarrollo/solicitudes_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Analizar solicitud")
@miembro_proyecto()
@miembro_comite()
def analizar_solicitud_view(request, id_proyecto, id_solicitud):
    """
    ::
    
        La vista para analizar una solicitud de cambio. Se deben cumplir los siguientes requisitos para utilizar esta vista:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Crear solicitud.
            - Debe ser miembro del proyecto en cuestion.
            
        Esta vista permite al usuario visualizar todos los campos de una solicitud de cambio. Ademas, en el template generado por 
        la vista, otorga los botones necesarios para votar la solicitud.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            - id_solicitud: el identificador de la solicitud de cambio.
            
        La vista retorna lo siguiente:
    
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    solicitud = SolicitudCambio.objects.filter(proyecto=proyecto).get(id=id_solicitud)
    relaciones = solicitud.item.relaciones.all()
    costo_monetario = solicitud.item.costo_monetario
    costo_temporal = solicitud.item.costo_temporal
    posee_hijos = False
    usuario_ya_voto = False
    solicitud_concretada = False
    
    # Comprobamos si el usuario miembro del comite ya realizado su voto.
    if str(request.user.id) in solicitud.votantes:
        usuario_ya_voto = True
    # Comprobamos si la solicitud ya ha sido aprobada o no.
    if solicitud.aprobada == False or solicitud.aprobada == True:
        solicitud_concretada = True
    
    # Verificamos si el item de la solicitud de cambio posee hijos/sucesores.
    if relaciones:
        posee_hijos = True
        
    if posee_hijos:
        # Cargamos en el listado hijos todos los hijos/sucesores del item de la solicitud de cambio.
        hijos = []
                            
        # Obtenemos todos los hijos/sucesores del item.
        while 1:
            nuevas_relaciones = []
            if len(relaciones) == 0:
                break
            for r in relaciones:
                hijos.append(r)
                if r.relaciones.count() > 0:
                    for h in r.relaciones.all():
                        nuevas_relaciones.append(h)
                relaciones = nuevas_relaciones
    
        # Calculamos el costo de impacto monetario y temporal del item de la solicitud.
        for h in hijos:
            costo_monetario = costo_monetario + h.costo_monetario
            costo_temporal = costo_temporal + h.costo_temporal
    
    # Creamos el grafo de relaciones del item de la solicitud de cambio.
    fases = proyecto.fases.all()
    grafo_relaciones = pydot.Dot(graph_type='digraph', fontname="Verdana", rankdir="TB")
    grafo_relaciones.set_node_defaults(style="filled", fillcolor="white", shape="record")
    grafo_relaciones.set_edge_defaults(color="black", arrowhead="vee")
    
    for f in fases:
        cluster_fase = pydot.Cluster("fase"+str(f.id),
                                     label="Fase: " + str(f.nombre), 
                                     shape='rectangle', 
                                     fontsize=15, 
                                     style='filled', 
                                     color='#E6E6E6', 
                                     fillcolor="#BDBDBD", 
                                     fontcolor="white")
        items = f.items.exclude(estado=2).filter(linea_base=None)
        if items:
            for i in items:
                if i == solicitud.item:
                    color_estado = "white"
                    if i.estado == 1:
                        color_estado = "#80FF00"
                    elif i.estado == 3:
                        color_estado = "#045FB4"
                    
                    cluster_fase.add_node(pydot.Node("item"+str(i.id),
                                          label = "<f0>Item: %s|<f1>Costo: %d"%(i.nombre, i.costo_monetario),
                                          fillcolor=color_estado, 
                                          fontsize=15))
                if posee_hijos:
                    if i in hijos:
                        color_estado = "white"
                        if i.estado == 1:
                            color_estado = "#80FF00"
                        elif i.estado == 3:
                            color_estado = "#045FB4"
                        
                        cluster_fase.add_node(pydot.Node("item"+str(i.id),
                                              label = "<f0>Item: %s|<f1>Costo: %d"%(i.nombre, i.costo_monetario),
                                              fillcolor=color_estado, 
                                              fontsize=15))
                
        items = f.items.exclude(linea_base=None)
        if items:
            lineas_base = f.lineas_base.all().exclude(estado=2)
            for lb in lineas_base:
                cluster_linea_base = pydot.Cluster("lb"+str(lb.id), 
                                                   label="Linea base: " + str(lb.nombre), 
                                                   shape='rectangle', 
                                                   fontsize=15, 
                                                   style='filled', 
                                                   color='#E6E6E6', 
                                                   fillcolor="#FFFFFF", 
                                                   fontcolor="black")
                items = lb.items.all()
                for i in items:
                    if i == solicitud.item:
                        if i.estado == 1:
                            color_estado = "#80FF00"
                        elif i.estado == 2:
                            color_estado = "#DF0101"
                        else:
                            color_estado = "#045FB4"
                        
                        cluster_linea_base.add_node(pydot.Node("item"+str(i.id), 
                                                               label = "<f0>Item: %s|<f1>Costo: %d"%(i.nombre, i.costo_monetario), 
                                                               fillcolor=color_estado, 
                                                               fontsize=15))
                        
                    if posee_hijos:
                        if i in hijos:
                            if i.estado == 1:
                                color_estado = "#80FF00"
                            elif i.estado == 2:
                                color_estado = "#DF0101"
                            else:
                                color_estado = "#045FB4"
                            
                            cluster_linea_base.add_node(pydot.Node("item"+str(i.id), 
                                                                   label = "<f0>Item: %s|<f1>Costo: %d"%(i.nombre, i.costo_monetario), 
                                                                   fillcolor=color_estado, 
                                                                   fontsize=15))
                cluster_fase.add_subgraph(cluster_linea_base)
            
        grafo_relaciones.add_subgraph(cluster_fase)

    for f in fases:
        items = f.items.all()
        for i in items:
            if i == solicitud.item:
                relaciones = i.relaciones.all()
                for r in relaciones:
                    grafo_relaciones.add_edge(pydot.Edge("item"+str(i.id), "item"+str(r.id), 
                                                       label='costo='+str(i.costo_monetario), 
                                                       fontsize=10))
            if posee_hijos:
                if i in hijos:
                    relaciones = i.relaciones.all()
                    for r in relaciones:
                        grafo_relaciones.add_edge(pydot.Edge("item"+str(i.id), "item"+str(r.id), 
                                                           label='costo='+str(i.costo_monetario), 
                                                           fontsize=10))
    # La direccion del grafico png que representa al grafo de relaciones del item de la solicitud de cambio.
    ruta_grafo = str(settings.MEDIA_ROOT) + "grafos/grafo_relaciones_item_" + str(solicitud.item.nombre) + ".png"
    grafo_relaciones.write(ruta_grafo, prog='dot', format='png')
    ruta_grafo = str(settings.MEDIA_URL) + "grafos/grafo_relaciones_item_" + str(solicitud.item.nombre) + ".png"
    
    if request.method == "POST":
        eleccion = request.POST.get('eleccion')
        
        # Si el usuario todavia no voto y la solicitud de cambio no ha sido concretada.
        if usuario_ya_voto == False and solicitud_concretada == False:
            # Si el voto fue negativo
            if eleccion == "0":
                solicitud.votos = solicitud.votos - 1
                solicitud.votantes = solicitud.votantes + str(request.user.id)
                solicitud.save()
            # Si el voto fue positivo
            elif eleccion == "1":
                solicitud.votos = solicitud.votos + 1
                solicitud.votantes = solicitud.votantes + str(request.user.id)
                solicitud.save()
                
            usuario_ya_voto = True
            # Si todos los miembros del comite ya han votado la solicitud de cambio.
            if len(solicitud.votantes) == proyecto.comite_de_cambios.count():
                # Si la cantidad final de votos es positiva.
                if solicitud.votos > 0:
                    solicitud.aprobada = True
                    item = solicitud.item
                    item.linea_base = None
                    item.estado = 0
                    item.version = item.version + 1
                    item.save()
                        
                    # Guardamos una version del item de la solicitud de cambio
                    version_item = VersionItem.objects.create(version=item.version, id_item=item.id, nombre=item.nombre,
                                                              descripcion=item.descripcion, costo_monetario=item.costo_monetario,
                                                              costo_temporal=item.costo_temporal, complejidad=item.complejidad,
                                                              estado=item.estado, fase=item.fase, tipo_item=item.tipo_item,
                                                              adan=item.adan, cain=item.cain, tipo_relacion=item.tipo_relacion,
                                                              fecha_version=datetime.datetime.now())
                    if item.padre:
                        version_item.padre = item.padre.id
                    if item.linea_base:
                        version_item.linea_base = item.linea_base
                    version_item.save()
                        
                    if posee_hijos:
                        # Por cada item hijo/sucesor, cambiamos su estado a En revision. Ademas guardamos, por cada uno, una version.  
                        for h in hijos:
                            h.estado = 3
                            h.version = h.version + 1
                            h.save()
                                    
                            version_h = VersionItem.objects.create(version=h.version, id_item=h.id, nombre=h.nombre, 
                                                                    descripcion=h.descripcion, costo_monetario=h.costo_monetario, 
                                                                    costo_temporal=h.costo_temporal, complejidad=h.complejidad,
                                                                    estado=h.estado, fase=h.fase, tipo_item=h.tipo_item,
                                                                    adan=h.adan, cain=h.cain, tipo_relacion=h.tipo_relacion, 
                                                                    fecha_version=datetime.datetime.now())
                            if h.padre:
                                version_h.padre = h.padre.id
                            if h.linea_base:
                                version_h.linea_base = h.linea_base
                            version_h.save()
                # Si la cantidad de votos final es negativa.
                else:
                    solicitud.aprobada = False
                # Guardamos los cambios hechos en la solicitud de cambio.    
                solicitud.save()
                
    cant_votos = len(solicitud.votantes)
    ctx = {'solicitud':solicitud, 'proyecto':proyecto, 'ruta_grafo':ruta_grafo, 'costo_monetario':costo_monetario, 'costo_temporal':costo_temporal, 'usuario_ya_voto':usuario_ya_voto, 'solicitud_concretada':solicitud_concretada, 'cant_votos':cant_votos}
    return render_to_response('desarrollo/analizar_solicitud.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear solicitud")
@miembro_proyecto()
def crear_solicitud_view(request, id_proyecto, id_fase, id_item):
    """
    ::
    
        La vista de creacion de una solicitud de cambio. Se deben cumplir los siguientes requisitos para utilizar esta vista:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Crear solicitud.
            - Debe ser miembro del proyecto en cuestion.
            
        Esta vista permite al usuario crear una solicitud de cambio para alterar un item bloqueado de una fase en curso.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            - id_fase: el identificador de la fase.
            - id_linea_base: el identificador de la linea base.
            - id_item: el identificador del item.
            
        La vista retorna lo siguiente:
    
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    item = fase.items.get(id=id_item)
    existe_lb = False
    
    if item.linea_base:
        existe_lb = True
    
    form = CrearSolicitudForm()
    if request.method == "POST":
        form = CrearSolicitudForm(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            accion = form.cleaned_data['accion']
            if accion == "1":
                accion = "Modificar item"
            elif accion == "2":
                accion = "Eliminar item"
            elif accion == "3":
                accion = "Agregar relacion a item"
            elif accion == "4":
                accion = "Quitar relacion de item"
            else:
                accion = "Reversionar item"
            
            # Borramos cualquier solicitud del mismo item y con la misma accion (si es que existe).
            solicitudes_item = SolicitudCambio.objects.filter(item=item)
            if solicitudes_item:
                existe_solicitud = True
                try:
                    solicitud = solicitudes_item.get(accion=accion)
                except SolicitudCambio.DoesNotExist:
                    existe_solicitud = False
                if existe_solicitud:
                    solicitud.delete()
            
            solicitud = SolicitudCambio.objects.create(usuario=request.user, proyecto=proyecto, 
                                                       fase=fase, linea_base=None, 
                                                       item=item, descripcion=descripcion,
                                                       votantes="", votos=0, accion=accion, 
                                                       fecha_emision=datetime.datetime.now())
            if existe_lb:
                solicitud.linea_base = item.linea_base
            
            solicitud.save()
            return HttpResponseRedirect('/desarrollo/fases/items/fase/%s/proyecto/%s'%(id_fase, id_proyecto))
        
    if existe_lb:
        ctx = {'item':item, 'linea_base':item.linea_base, 'fase':fase, 'proyecto':proyecto, 'form':form}
    else:
        ctx = {'item':item, 'fase':fase, 'proyecto':proyecto, 'form':form}
        
    return render_to_response('desarrollo/crear_solicitud.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar solicitudes de usuario")
@miembro_proyecto()
def solicitudes_usuario_view(request, id_proyecto, id_usuario):
    """
    ::
    
        La vista de gestion de solicitudes de cambio de un usuario. Se deben cumplir los siguientes requisitos para utilizar esta vista:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Gestionar solicitudes de usuario.
            - Debe ser miembro del proyecto en cuestion.
            
        Esta vista permite a un usuario cualquiera gestionar todas sus solicitudes de cambio enviadas. 
        Se cargan todas las solicitudes del usuario y se envian como un listado al template de gestion de solicitudes del usuario.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
    
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    solicitudes = SolicitudCambio.objects.filter(proyecto=proyecto).filter(usuario=request.user)
    ctx = {'proyecto':proyecto, 'solicitudes':solicitudes}
    return render_to_response('desarrollo/solicitudes_usuario.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Visualizar solicitud")
@miembro_proyecto()
def visualizar_solicitud_view(request, id_proyecto, id_solicitud):
    """
    ::
    
        La vista de visualizacion de solicitud de cambio. Se deben cumplir los siguientes requisitos para utilizar esta vista:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Visualizar solicitud.
            - Debe ser miembro del proyecto en cuestion.
            
        Esta vista permite a un usuario cualquiera visualizar cada una de sus solicitudes de cambio enviadas. 
        Se cargan todos los campos de la solicitud de cambio mas un grafico que muestra las relaciones del item de la solicitud.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            - id_solicitud: el identificador de la solicitud de cambio.
            
        La vista retorna lo siguiente:
    
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    solicitud = SolicitudCambio.objects.filter(proyecto=proyecto).filter(usuario=request.user).get(id=id_solicitud)
    relaciones = solicitud.item.relaciones.all()
    costo_monetario = solicitud.item.costo_monetario
    costo_temporal = solicitud.item.costo_temporal
    posee_hijos = False
    
    if relaciones:
        posee_hijos = True
        
    if posee_hijos:
        resultados = []
                            
        # Obtenemos todos los hijos/sucesores del item.
        while 1:
            nuevas_relaciones = []
            if len(relaciones) == 0:
                break
            for r in relaciones:
                resultados.append(r)
                if r.relaciones.count() > 0:
                    for h in r.relaciones.all():
                        nuevas_relaciones.append(h)
                relaciones = nuevas_relaciones
    
    if posee_hijos:
        # Calculamos el costo de impacto monetario y temporal del item de la solicitud.
        for r in resultados:
            costo_monetario = costo_monetario + r.costo_monetario
            costo_temporal = costo_temporal + r.costo_temporal
    
    fases = proyecto.fases.all()
    grafo_relaciones = pydot.Dot(graph_type='digraph', fontname="Verdana", rankdir="TB")
    grafo_relaciones.set_node_defaults(style="filled", fillcolor="white", shape="record")
    grafo_relaciones.set_edge_defaults(color="black", arrowhead="vee")
    
    for f in fases:
        cluster_fase = pydot.Cluster("fase"+str(f.id),
                                     label="Fase: " + str(f.nombre), 
                                     shape='rectangle', 
                                     fontsize=15, 
                                     style='filled', 
                                     color='#E6E6E6', 
                                     fillcolor="#BDBDBD", 
                                     fontcolor="white")
        items = f.items.exclude(estado=2).filter(linea_base=None)
        if items:
            for i in items:
                if i == solicitud.item:
                    color_estado = "white"
                    if i.estado == 1:
                        color_estado = "#80FF00"
                    elif i.estado == 3:
                        color_estado = "#045FB4"
                    
                    cluster_fase.add_node(pydot.Node("item"+str(i.id),
                                          label = "<f0>Item: %s|<f1>Costo: %d"%(i.nombre, i.costo_monetario),
                                          fillcolor=color_estado, 
                                          fontsize=15))
                if posee_hijos:
                    if i in resultados:
                        color_estado = "white"
                        if i.estado == 1:
                            color_estado = "#80FF00"
                        elif i.estado == 3:
                            color_estado = "#045FB4"
                        
                        cluster_fase.add_node(pydot.Node("item"+str(i.id),
                                              label = "<f0>Item: %s|<f1>Costo: %d"%(i.nombre, i.costo_monetario),
                                              fillcolor=color_estado, 
                                              fontsize=15))
                
        items = f.items.exclude(linea_base=None)
        if items:
            lineas_base = f.lineas_base.all().exclude(estado=2)
            for lb in lineas_base:
                cluster_linea_base = pydot.Cluster("lb"+str(lb.id), 
                                                   label="Linea base: " + str(lb.nombre), 
                                                   shape='rectangle', 
                                                   fontsize=15, 
                                                   style='filled', 
                                                   color='#E6E6E6', 
                                                   fillcolor="#FFFFFF", 
                                                   fontcolor="black")
                items = lb.items.all()
                for i in items:
                    if i == solicitud.item:
                        if i.estado == 1:
                            color_estado = "#80FF00"
                        elif i.estado == 2:
                            color_estado = "#DF0101"
                        else:
                            color_estado = "#045FB4"
                        
                        cluster_linea_base.add_node(pydot.Node("item"+str(i.id), 
                                                               label = "<f0>Item: %s|<f1>Costo: %d"%(i.nombre, i.costo_monetario), 
                                                               fillcolor=color_estado, 
                                                               fontsize=15))
                        
                    if posee_hijos:
                        if i in resultados:
                            if i.estado == 1:
                                color_estado = "#80FF00"
                            elif i.estado == 2:
                                color_estado = "#DF0101"
                            else:
                                color_estado = "#045FB4"
                            
                            cluster_linea_base.add_node(pydot.Node("item"+str(i.id), 
                                                                   label = "<f0>Item: %s|<f1>Costo: %d"%(i.nombre, i.costo_monetario), 
                                                                   fillcolor=color_estado, 
                                                                   fontsize=15))
                cluster_fase.add_subgraph(cluster_linea_base)
            
        grafo_relaciones.add_subgraph(cluster_fase)

    for f in fases:
        items = f.items.all()
        for i in items:
            if i == solicitud.item:
                relaciones = i.relaciones.all()
                for r in relaciones:
                    grafo_relaciones.add_edge(pydot.Edge("item"+str(i.id), "item"+str(r.id), 
                                                       label='costo='+str(i.costo_monetario), 
                                                       fontsize=10))
            if posee_hijos:
                if i in resultados:
                    relaciones = i.relaciones.all()
                    for r in relaciones:
                        grafo_relaciones.add_edge(pydot.Edge("item"+str(i.id), "item"+str(r.id), 
                                                           label='costo='+str(i.costo_monetario), 
                                                           fontsize=10))
                        
    ruta_grafo = str(settings.MEDIA_ROOT) + "grafos/grafo_relaciones_item_" + str(solicitud.item.nombre) + ".png"
    grafo_relaciones.write(ruta_grafo, prog='dot', format='png')
    ruta_grafo = str(settings.MEDIA_URL) + "grafos/grafo_relaciones_item_" + str(solicitud.item.nombre) + ".png"
    
    ctx = {'proyecto':proyecto, 'solicitud':solicitud, 'ruta_grafo':ruta_grafo, 'costo_monetario':costo_monetario, 'costo_temporal':costo_temporal}
    return render_to_response('desarrollo/visualizar_solicitud.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Cancelar solicitud")
@miembro_proyecto()
def cancelar_solicitud_view(request, id_proyecto, id_solicitud):
    """
    ::
    
        La vista de cancelacion de una solicitud de cambio. Se deben cumplir los siguientes requisitos para utilizar esta vista:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Cancelar solicitud.
            - Debe ser miembro del proyecto en cuestion.
            
        Esta vista permite a un usuario cualquiera cancelar una de sus solicitudes de cambio enviadas. 
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            - id_solicitud: el identificador de la solicitud de cambio.
            
        La vista retorna lo siguiente:
    
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    solicitud = SolicitudCambio.objects.filter(proyecto=proyecto).filter(usuario=request.user).get(id=id_solicitud)
    solicitud.delete()
    
    ctx = {'proyecto':proyecto}
    return render_to_response('desarrollo/cancelar_solicitud.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar fases de proyecto")
@miembro_proyecto()
def fases_proyecto_view(request, id_proyecto):
    """
    ::
    
        La vista del listado de fases por proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
                - El usuario debe estar logueado.
                - El usuario debe poseer el permiso: Gestionar fases de proyecto.
                - Debe ser miembro del proyecto en cuestion.
        
        Esta vista permite al usuario listar y conocer las opciones de las fases por proyecto.
        Inicialmente, se verifican los permisos del usuario solicitante para restringir (si es necesario) 
        los botones de accion sobre cada fase.
                
        La vista recibe los siguientes parametros:
    
                - request: contiene informacion sobre la sesion actual.
                - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
                - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    gestionar_tipos_item = False
    gestionar_lineas_base = False
    gestionar_items = False
    gestionar_roles = False
    iniciar_fase = False
    finalizar_fase = False
    roles = request.user.roles.all()
    for r in roles:
        for p in r.permisos.all():
            if p.nombre == 'Gestionar tipos de item de fase':
                gestionar_tipos_item = True
            elif p.nombre == 'Gestionar roles de fase':
                gestionar_roles = True
            elif p.nombre == 'Iniciar fase':
                iniciar_fase = True
            elif p.nombre == 'Finalizar fase':
                finalizar_fase = True
            elif p.nombre == 'Gestionar items de fase':
                gestionar_items = True
            elif p.nombre == 'Gestionar lineas base de fase':
                gestionar_lineas_base = True
                
            if gestionar_tipos_item and gestionar_roles and iniciar_fase and finalizar_fase and gestionar_items and gestionar_lineas_base:
                break
        if gestionar_tipos_item and gestionar_roles and iniciar_fase and finalizar_fase and gestionar_items and gestionar_lineas_base:
                break
            
    fases = proyecto.fases.all()
    grafo_proyecto = pydot.Dot(graph_type='digraph', fontname="Verdana", rankdir="TB")
    grafo_proyecto.set_node_defaults(style="filled", fillcolor="white", shape="record")
    grafo_proyecto.set_edge_defaults(color="black", arrowhead="vee")
    
    for f in fases:
        cluster_fase = pydot.Cluster("fase"+str(f.id),
                                     label="Fase: " + str(f.nombre), 
                                     shape='rectangle', 
                                     fontsize=15, 
                                     style='filled', 
                                     color='#E6E6E6', 
                                     fillcolor="#BDBDBD", 
                                     fontcolor="white")
        items = f.items.exclude(estado=2).filter(linea_base=None)
        if items:
            for i in items:
                color_estado = "white"
                if i.estado == 1:
                    color_estado = "#80FF00"
                elif i.estado == 3:
                    color_estado = "#045FB4"
                
                cluster_fase.add_node(pydot.Node("item"+str(i.id),
                                      label = "<f0>Item: %s|<f1>Costo: %d"%(i.nombre, i.costo_monetario),
                                      fillcolor=color_estado, 
                                      fontsize=15))
        items = f.items.exclude(linea_base=None)
        if items:
            lineas_base = f.lineas_base.all().exclude(estado=2)
            for lb in lineas_base:
                cluster_linea_base = pydot.Cluster("lb"+str(lb.id), 
                                                   label="Linea base: " + str(lb.nombre), 
                                                   shape='rectangle', 
                                                   fontsize=15, 
                                                   style='filled', 
                                                   color='#E6E6E6', 
                                                   fillcolor="#FFFFFF", 
                                                   fontcolor="black")
                items = lb.items.all()
                for i in items:
                    if i.estado == 1:
                        color_estado = "#80FF00"
                    elif i.estado == 2:
                        color_estado = "#DF0101"
                    else:
                        color_estado = "#045FB4"
                    
                    cluster_linea_base.add_node(pydot.Node("item"+str(i.id), 
                                                           label = "<f0>Item: %s|<f1>Costo: %d"%(i.nombre, i.costo_monetario), 
                                                           fillcolor=color_estado, 
                                                           fontsize=15))
                cluster_fase.add_subgraph(cluster_linea_base)
            
        grafo_proyecto.add_subgraph(cluster_fase)

    for f in fases:
        items = f.items.all()
        for i in items:
            relaciones = i.relaciones.all()
            for r in relaciones:
                grafo_proyecto.add_edge(pydot.Edge("item"+str(i.id), "item"+str(r.id), 
                                                   label='costo='+str(i.costo_monetario), 
                                                   fontsize=10))
            
    ruta_grafo = str(settings.MEDIA_ROOT) + "grafos/grafo_proyecto_" + str(proyecto.nombre) + ".png"
    grafo_proyecto.write(ruta_grafo, prog='dot', format='png')
    ruta_grafo = str(settings.MEDIA_URL) + "grafos/grafo_proyecto_" + str(proyecto.nombre) + ".png"

    ctx = {'fases':fases, 'proyecto':proyecto, 'ruta_grafo':ruta_grafo, 'gestionar_tipos_item':gestionar_tipos_item, 'gestionar_roles':gestionar_roles, 'iniciar_fase':iniciar_fase, 'finalizar_fase':finalizar_fase, 'gestionar_items':gestionar_items, 'gestionar_lineas_base':gestionar_lineas_base}
    return render_to_response('desarrollo/gestion_fases.html', ctx, context_instance=RequestContext(request))    

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar roles de fase")
@miembro_proyecto()
@rol_fase_requerido()
def roles_fase_view(request, id_proyecto, id_fase):
    """
    ::
    
        La vista del listado de roles por fase. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Gestionar roles de fase.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario listar y conocer las opciones de los roles de la fase previamente seleccionada.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    fase = Fase.objects.get(id=id_fase)
    proyecto = Proyecto.objects.get(id=id_proyecto)
    roles = Rol.objects.filter(fase__id=id_fase)
    ctx = {'fase':fase, 'proyecto':proyecto, 'roles':roles}
    return render_to_response('fase/roles_fase.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@miembro_proyecto()
@rol_fase_requerido()
def fase_agregar_rol_view(request, id_proyecto, id_fase):
    """
    ::
    
        La vista del listado de roles del proyecto ligado a la fase. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            
        Esta vista permite al usuario listar todos los roles del proyecto al cual esta ligada la fase, ademas, el template relacionado concede 
        las opciones para agregar un rol seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    fase = Fase.objects.get(id=id_fase)
    proyecto = fase.proyecto
    roles = proyecto.roles.all()
    estado_valido = True
    
    if fase.estado == 1 or fase.estado == 2:
        estado_valido = False
    
    ctx = {'fase':fase, 'proyecto':proyecto, 'roles':roles, 'estado_valido':estado_valido}
    return render_to_response('fase/agregar_rol.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar rol a fase")
@miembro_proyecto()
@rol_fase_requerido()
def fase_confirmacion_agregar_rol_view(request, id_proyecto, id_fase, id_rol):
    """
    ::
    
        La vista de confirmacion de agregacion de un rol a una fase. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Agregar rol a fase.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario agregar un rol seleccionado a la fase seleccionada previamente. Se verifica si el rol a agregar ya 
        pertenece a la fase, en cuyo caso se cancelara la operacion.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_rol: el identificador del rol.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    fase = Fase.objects.get(id=id_fase)
    proyecto = fase.proyecto
    rol = Rol.objects.get(id=id_rol)
    estado_valido = True
    existe_rol = True
    
    if fase.estado == 1 or fase.estado == 2:
        estado_valido = False
    
    try:
        role = fase.roles.get(id=id_rol)
    except Rol.DoesNotExist:
        existe_rol = False
             
    if estado_valido and existe_rol == False:
        fase.roles.add(rol)
        fase.save()
    ctx = {'fase':fase, 'rol':rol, 'proyecto':proyecto, 'estado_valido':estado_valido, 'existe_rol':existe_rol}
    return render_to_response('fase/confirmacion_agregar_rol.html', ctx, context_instance=RequestContext(request))  
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Quitar rol de fase")
@miembro_proyecto()
@rol_fase_requerido()
def fase_quitar_rol_view(request, id_proyecto, id_fase, id_rol):
    """
    ::
    
        La vista para quitar un rol de una fase. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Quitar rol de fase.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
        
        Esta vista permite al usuario quitar un rol seleccionado de la fase seleccionada previamente.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_rol: el identificador del rol.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    fase = Fase.objects.get(id=id_fase)
    proyecto = fase.proyecto
    rol = Rol.objects.get(id=id_rol)
    estado_valido = True
    
    if fase.estado == 1 or fase.estado == 2:
        estado_valido = False
    
    if estado_valido:
        fase.roles.remove(rol)
        fase.save()
    ctx = {'fase':fase, 'rol':rol, 'proyecto':proyecto, 'estado_valido':estado_valido}
    return render_to_response('fase/quitar_rol.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar tipos de item de fase")
@miembro_proyecto()
@rol_fase_requerido()
def tipos_item_fase_view(request, id_proyecto, id_fase):
    """
    ::
    
        La vista del listado de tipos de item del sistema. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
                - El usuario debe estar logueado.
                - El usuario debe poseer el permiso: Gestionar tipos de item de fase.
                - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
                
        Esta vista permite al usuario listar y conocer las opciones de los tipos de item del sistema.
        Inicialmente, se verifican los permisos del usuario solicitante para restringir (si es necesario) 
        los botones de accion sobre cada tipo de item.
                
        La vista recibe los siguientes parametros:
    
                - request: contiene informacion sobre la sesion actual.
                - id_fase: el identificador de la fase.
                - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
                - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    crear_tipo_de_item = False
    modificar_tipo_de_item = False
    eliminar_tipo_de_item = False
    visualizar_tipo_de_item = False
    gestionar_tipos_de_atributo = False
    roles = request.user.roles.all()
    for r in roles:
        for p in r.permisos.all():
            if p.nombre == 'Crear tipo de item':
                crear_tipo_de_item = True
            elif p.nombre == 'Modificar tipo de item':
                modificar_tipo_de_item = True
            elif p.nombre == 'Eliminar tipo de item':
                eliminar_tipo_de_item = True
            elif p.nombre == 'Visualizar tipo de item':
                visualizar_tipo_de_item = True
            elif p.nombre == 'Gestionar tipos de atributo de tipo de item':
                gestionar_tipos_de_atributo = True
                
            if crear_tipo_de_item and modificar_tipo_de_item and eliminar_tipo_de_item and visualizar_tipo_de_item and gestionar_tipos_de_atributo:
                break
        if crear_tipo_de_item and modificar_tipo_de_item and eliminar_tipo_de_item and visualizar_tipo_de_item and gestionar_tipos_de_atributo:
                break
            
    tipos_item = fase.tipos_item.all()
    ctx = {'tipos_item':tipos_item, 'fase':fase, 'proyecto':proyecto, 'crear_tipo_de_item':crear_tipo_de_item, 'modificar_tipo_de_item':modificar_tipo_de_item, 'eliminar_tipo_de_item':eliminar_tipo_de_item, 'visualizar_tipo_de_item':visualizar_tipo_de_item, 'gestionar_tipos_de_atributo':gestionar_tipos_de_atributo}
    return render_to_response('tipo_item/gestion_tipos_item.html', ctx, context_instance=RequestContext(request))
  
@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear tipo de item")
@miembro_proyecto()
@rol_fase_requerido()
def crear_tipo_item_view(request, id_proyecto, id_fase):
    """
    ::
    
        La vista para crear un tipo de item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Crear tipo de item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario crear un tipo de item para lograr esto, se verifica la validez de cada campo ingresado y 
        luego se crea el tipo de item de acuerdo a los campos ingresados. 
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de usuarios. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    estado_valido = True
    
    if fase.estado == 1 or fase.estado == 2:
        estado_valido = False
    
    form = CrearTipoItemForm()
    if estado_valido:
        if request.method == "POST":
            form = CrearTipoItemForm(request.POST)
            if form.is_valid():
                nombre = form.cleaned_data['nombre']
                descripcion = form.cleaned_data['descripcion']
                
                tipo_item = TipoItem.objects.create(nombre=nombre, descripcion=descripcion)
                tipo_item.save()
                fase.tipos_item.add(tipo_item)
                fase.save()
                return HttpResponseRedirect('/desarrollo/fases/tipos_item/fase/%s/proyecto/%s'%(id_fase, id_proyecto))
                
            else:
                ctx = {'form':form, 'fase':fase, 'proyecto':proyecto, 'estado_valido':estado_valido}
            return render_to_response('tipo_item/crear_tipo_item.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form, 'fase':fase, 'proyecto':proyecto, 'estado_valido':estado_valido}
    return render_to_response('tipo_item/crear_tipo_item.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Modificar tipo de item")
@miembro_proyecto()
@rol_fase_requerido()
def modificar_tipo_item_view(request, id_proyecto, id_fase, id_tipo_item):
    """
    ::
    
        La vista para modificar un tipo de item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Modificar tipo de item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario modificar un tipo de item previamente seleccionada, para lograr esto, 
        se verifica la validez de cada campo modificado y luego se guarda el tipo de item de acuerdo a los campos ingresados.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_tipo_item: el identificador del tipo de item.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template de visualizacion de la fase modificada. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    tipo_item = fase.tipos_item.get(id=id_tipo_item)
    estado_valido = True
    
    if fase.estado == 1 or fase.estado == 2:
        estado_valido = False
    
    if estado_valido:
        if request.method == "POST":
            form = ModificarTipoItemForm(data=request.POST)
            if form.is_valid():
                nombre = form.cleaned_data['nombre']
                descripcion = form.cleaned_data['descripcion']
                
                tipo_item.nombre = nombre
                tipo_item.descripcion = descripcion
    
                tipo_item.save()
                return HttpResponseRedirect('/desarrollo/fases/tipos_item/tipo_item/%s/fase/%s/proyecto/%s'%(tipo_item.id, id_fase, id_proyecto))
            
    if request.method == "GET":
        form = ModificarTipoItemForm(initial={
            'nombre': tipo_item.nombre,
            'descripcion': tipo_item.descripcion,
            })
    ctx = {'form': form, 'tipo_item': tipo_item, 'fase':fase, 'proyecto':proyecto, 'estado_valido':estado_valido}
    return render_to_response('tipo_item/modificar_tipo_item.html', ctx, context_instance=RequestContext(request))
  
@login_required(login_url='/login/')
@permiso_requerido(permiso="Visualizar tipo de item")
@miembro_proyecto()
@rol_fase_requerido()
def visualizar_tipo_item_view(request, id_proyecto, id_fase, id_tipo_item):
    """
    ::
    
        La vista para visualizar un tipo de item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Visualizar tipo de item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario visualizar todos los campos guardados de un tipo de item previamente seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_tipo_item: el identificador del tipo de item.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    tipo_item = fase.tipos_item.get(id=id_tipo_item)
    ctx = {'tipo_item': tipo_item, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('tipo_item/visualizar_tipo_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Eliminar tipo de item")
@miembro_proyecto()
@rol_fase_requerido()
def eliminar_tipo_item_view(request, id_proyecto, id_fase, id_tipo_item):
    """
    ::
    
        La vista para eliminar un tipo de item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Eliminar tipo de item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario eliminar un tipo de item previamente seleccionado.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_tipo_item: el identificador del tipo de item.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o no se cumplieron las condiciones para eliminar, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de fases. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    tipo_item = fase.tipos_item.get(id=id_tipo_item)
    estado_valido = True
    
    if fase.estado == 1 or fase.estado == 2:
        estado_valido = False
    
    if estado_valido:
        if request.method == "POST":
            tipo_item.delete()
            return HttpResponseRedirect('/desarrollo/fases/tipos_item/fase/%s/proyecto/%s'%(id_fase, id_proyecto))
        
    if request.method == "GET":
        ctx = {'tipo_item':tipo_item, 'fase':fase, 'proyecto':proyecto, 'estado_valido':estado_valido}
        return render_to_response('tipo_item/eliminar_tipo_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar tipos de atributo de tipo de item")
@miembro_proyecto()
@rol_fase_requerido()
def tipos_atributo_tipo_item_view(request, id_proyecto, id_fase, id_tipo_item):
    """
    ::
    
        La vista del listado de tipos de atributo del tipo de item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Gestionar tipos de atributo de tipo de item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario listar y conocer las opciones de los tipos de atributo del item previamente seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_tipo_item: el identificador del tipo de item.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    fase = Fase.objects.get(id=id_fase)
    proyecto = fase.proyecto
    tipo_item = TipoItem.objects.get(id=id_tipo_item)
    tipos_atributo = TipoAtributo.objects.filter(tipoitem__id=id_tipo_item)
    ctx = {'tipo_item':tipo_item, 'tipos_atributo':tipos_atributo, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('tipo_item/tipos_atributo_tipo_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@miembro_proyecto()
@rol_fase_requerido()
def agregar_tipo_atributo_view(request, id_proyecto, id_fase, id_tipo_item):
    """
    ::
    
        La vista del listado de tipos de atributo ligados al tipo de item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario listar todos los tipos de atributo del sistema, ademas, el template relacionado concede 
        las opciones para agregar un tipo de atributo seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_tipo_item: el identificador del tipo de item.
            - id_fase: el identificador del la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    fase = Fase.objects.get(id=id_fase)
    proyecto = fase.proyecto
    tipo_item = TipoItem.objects.get(id=id_tipo_item)
    tipos_atributo = TipoAtributo.objects.all()
    estado_valido = True
    
    if fase.estado == 1 or fase.estado == 2:
        estado_valido = False
    
    ctx = {'tipo_item':tipo_item, 'tipos_atributo':tipos_atributo, 'fase':fase, 'proyecto':proyecto, 'estado_valido':estado_valido}
    return render_to_response('tipo_item/agregar_tipo_atributo.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar tipo de atributo a tipo de item")
@miembro_proyecto()
@rol_fase_requerido()
def confirmacion_agregar_tipo_atributo_view(request, id_proyecto, id_fase, id_tipo_atributo, id_tipo_item):
    """
    ::
    
        La vista de confirmacion de agregacion de un tipo de atributo a un tipo de item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Agregar tipo de atributo a tipo de item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario agregar un tipo de atributo seleccionado a el tipo de item seleccionado previamente. Se verifica si el tipo de atributo a agregar ya 
        pertenece al tipo de item, en cuyo caso se cancelara la operacion.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_tipo_item: el identificador del tipo de item.
            - id_tipo_atributo: el identificador del tipo de atributo.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    fase = Fase.objects.get(id=id_fase)
    proyecto = fase.proyecto
    tipo_item = TipoItem.objects.get(id=id_tipo_item)
    tipo_atributo = TipoAtributo.objects.get(id=id_tipo_atributo)
    estado_valido = True
    existe_tipo_atributo = True
    
    if fase.estado == 1 or fase.estado == 2:
        estado_valido = False
    
    try:
        tipo_atribut = tipo_item.tipos_atributo.get(id=id_tipo_atributo)
    except TipoAtributo.DoesNotExist:
        existe_tipo_atributo = False
        
    if estado_valido and existe_tipo_atributo == False:
        tipo_item.tipos_atributo.add(tipo_atributo)
        tipo_item.save()
        
    ctx = {'tipo_item':tipo_item, 'tipo_atributo':tipo_atributo, 'fase':fase, 'proyecto':proyecto, 'estado_valido':estado_valido, 'existe_tipo_atributo':existe_tipo_atributo}
    return render_to_response('tipo_item/confirmacion_agregar_tipo_atributo.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Quitar tipo de atributo de tipo de item")
@miembro_proyecto()
@rol_fase_requerido()
def quitar_tipo_atributo_view(request, id_proyecto, id_fase, id_tipo_atributo, id_tipo_item):
    """
    ::
    
        La vista para quitar un tipo de atributo de un tipo de item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Quitar tipo de atributo de tipo de item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
        
        Esta vista permite al usuario quitar un tipo de atributo seleccionado del tipo de item seleccionado previamente.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_tipo_item: el identificador de la tipo de item.
            - id_tipo_atributo: el identificador del tipo de atributo.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    fase = Fase.objects.get(id=id_fase)
    proyecto = fase.proyecto
    tipo_item = TipoItem.objects.get(id=id_tipo_item)
    tipo_atributo = TipoAtributo.objects.get(id=id_tipo_atributo)
    atributos = ValorAtributo.objects.filter(tipo_atributo__id=id_tipo_atributo)
    estado_valido = True
    posee_atributos = False
    
    if fase.estado == 1 or fase.estado == 2:
        estado_valido = False
    
    if atributos:
        posee_atributos = True
        
    if estado_valido and posee_atributos == False:
        tipo_item.tipos_atributo.remove(tipo_atributo)
        tipo_item.save()
        
    ctx = {'tipo_item':tipo_item, 'tipo_atributo':tipo_atributo, 'fase':fase, 'proyecto':proyecto, 'estado_valido':estado_valido, 'posee_atributos':posee_atributos}
    return render_to_response('tipo_item/quitar_tipo_atributo.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Iniciar fase")
@miembro_proyecto()
@rol_fase_requerido()
def iniciar_fase_view(request, id_proyecto, id_fase):
    """
    ::
    
        La vista para iniciar una fase. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Iniciar fase.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario iniciar una fase si es que cumple con las siguientes condiciones:
        
            - Debe estar en estado Inactivo.
            - Debe poseer al menos un rol.
            - Debe poseer al menos un tipo de item.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    fase = Fase.objects.get(id=id_fase)
    proyecto = Proyecto.objects.get(id=id_proyecto)
    inicio_valido = True
    estado_valido = True
    roles_valido = True
    tipos_item_valido = True
    
    if fase.estado != 0:
        estado_valido = False
        inicio_valido = False
    if fase.tipos_item.count() == 0:
        tipos_item_valido = False
        inicio_valido = False
    if fase.roles.count() == 0:
        roles_valido = False
        inicio_valido = False
    
    if inicio_valido:
        fase.estado = 1
        fase.save()
        ctx = {'fase':fase, 'inicio_valido':inicio_valido, 'estado_valido':estado_valido, 'tipos_item_valido':tipos_item_valido, 'roles_valido':roles_valido, 'proyecto':proyecto}
        return render_to_response('fase/iniciar_fase.html', ctx, context_instance=RequestContext(request))
    else:
        ctx = {'fase':fase, 'inicio_valido':inicio_valido, 'estado_valido':estado_valido, 'tipos_item_valido':tipos_item_valido, 'roles_valido':roles_valido, 'proyecto':proyecto}
        return render_to_response('fase/iniciar_fase.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Finalizar fase")
@miembro_proyecto()
@rol_fase_requerido()
def finalizar_fase_view(request, id_proyecto, id_fase):
    """
    ::
    
        La vista para finalizar una fase. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Finalizar fase.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario finalizar una fase si es que cumple con las siguientes condiciones:
        
            - Debe estar en estado En curso.
            - Todos sus items deben estar en estado Bloqueado.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    finalizado_valido = True
    estado_valido = False
    secuencia_valida = True
    
    if fase.estado == 1:
        estado_valido = True
    
    if fase.num_secuencia > 1:
        num_secuencia = fase.num_secuencia - 1
        fase_anterior = proyecto.fases.get(num_secuencia=num_secuencia)
        if fase_anterior.estado != 2:
            secuencia_valida = False

    items = fase.items.all()
    for i in items:
        if i.estado != 2:
            finalizado_valido = False
            
    if finalizado_valido and secuencia_valida and estado_valido:
        fase.estado = 2
        fase.save()
        ctx = {'fase':fase, 'finalizado_valido':finalizado_valido, 'estado_valido':estado_valido, 'secuencia_valida':secuencia_valida, 'proyecto':proyecto}
        return render_to_response('fase/finalizar_fase.html', ctx, context_instance=RequestContext(request))
    else:
        ctx = {'fase':fase, 'finalizado_valido':finalizado_valido, 'estado_valido':estado_valido, 'secuencia_valida':secuencia_valida, 'proyecto':proyecto}
        return render_to_response('fase/finalizar_fase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar items de fase")
@miembro_proyecto()
@rol_fase_requerido()
def items_fase_view(request, id_proyecto, id_fase):
    """
    ::
    
        La vista del listado de items por fase. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Gestionar items de fase.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario listar y conocer las opciones de desarrollo de los items de la fase seleccionada.
        Inicialmente, se verifican los permisos del usuario solicitante para restringir (si es necesario) 
        los botones de accion sobre cada item.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    crear_item = False
    modificar_item = False
    eliminar_item = False
    visualizar_item = False
    gestionar_relaciones = False
    aprobar_item = False
    gestionar_versiones = False
    roles = request.user.roles.all()
    for r in roles:
        for p in r.permisos.all():
            if p.nombre == 'Crear item':
                crear_item = True
            elif p.nombre == 'Modificar item':
                modificar_item = True
            elif p.nombre == 'Eliminar item':
                eliminar_item = True
            elif p.nombre == 'Visualizar item':
                visualizar_item = True
            elif p.nombre == 'Gestionar relaciones de item':
                gestionar_relaciones = True
            elif p.nombre == 'Aprobar item':
                aprobar_item = True
            elif p.nombre == 'Gestionar versiones de item':
                gestionar_versiones = True
                
            if crear_item and modificar_item and eliminar_item and visualizar_item and gestionar_relaciones and aprobar_item and gestionar_versiones:
                break
        if crear_item and modificar_item and eliminar_item and visualizar_item and gestionar_relaciones and aprobar_item and gestionar_versiones:
            break
    
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    valido = True
    if fase.estado == 0:
        valido = False
    items = fase.items.all()
    ctx = {'valido':valido, 'proyecto':proyecto, 'fase':fase, 'items':items, 'crear_item':crear_item, 'modificar_item':modificar_item, 'eliminar_item':eliminar_item, 'visualizar_item':visualizar_item, 'gestionar_relaciones':gestionar_relaciones, 'aprobar_item':aprobar_item, 'gestionar_versiones':gestionar_versiones}
    return render_to_response('fase/items_fase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear item")
@miembro_proyecto()
@rol_fase_requerido()
def crear_item_view(request, id_proyecto, id_fase):
    """
    ::
    
        La vista para crear un item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Crear item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario crear y agregar un item a la fase previamente seleccionada, para lograr esto, 
        se verifica la validez de cada campo ingresado y luego se crea el item de acuerdo a los campos ingresados y 
        se almacena en la fase. 
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de items por fase. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    tipos_item = fase.tipos_item.all()
    estado_valido = True
    if fase.estado == 2:
        estado_valido = False
    
    form = CrearItemForm()
    if estado_valido:
        if request.method == "POST":
            form = CrearItemForm(request.POST)
            if form.is_valid():
                nombre = form.cleaned_data['nombre']
                descripcion = form.cleaned_data['descripcion']
                complejidad = form.cleaned_data['complejidad']
                costo_monetario = form.cleaned_data['costo_monetario']
                costo_temporal = form.cleaned_data['costo_temporal']
                
                id_tipo_item = request.POST.get('tipo_item')
                
                tipo_item = TipoItem.objects.get(id=id_tipo_item)
                
                item = Item.objects.create(nombre=nombre, descripcion=descripcion, complejidad=complejidad, costo_monetario=costo_monetario, costo_temporal=costo_temporal, tipo_item=tipo_item)
                tipos_atributo = tipo_item.tipos_atributo.all()
                for tipo_atributo in tipos_atributo:
                    valor_atributo = ValorAtributo.objects.create(item=item, tipo_item=tipo_item, tipo_atributo=tipo_atributo)
                    valor_atributo.save()
                fase.items.add(item)
                item.save()
                fase.save()
                version_item = VersionItem.objects.create(version=item.version, id_item=item.id, nombre=item.nombre, 
                                                          descripcion=item.descripcion, costo_monetario=item.costo_monetario, 
                                                          costo_temporal=item.costo_temporal, complejidad=item.complejidad,
                                                          estado=item.estado, fase=item.fase, tipo_item=item.tipo_item,
                                                          adan=item.adan, cain=item.cain, padre=item.padre,
                                                          tipo_relacion=item.tipo_relacion, fecha_version=datetime.datetime.now())
                version_item.save()
                
                return HttpResponseRedirect('/desarrollo/fases/items/fase/%s/proyecto/%s'%(id_fase, id_proyecto))
                
            else:
                ctx = {'form':form, 'fase':fase, 'proyecto':proyecto, 'tipos_item':tipos_item, 'estado_valido':estado_valido}
                return render_to_response('crear_item.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form, 'fase':fase, 'proyecto':proyecto, 'tipos_item':tipos_item, 'estado_valido':estado_valido}
    return render_to_response('item/crear_item.html', ctx, context_instance=RequestContext(request))

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def is_date(s):
    try:
        datetime.datetime.strptime(s, '%Y-%m-%d')
        return True
    except ValueError:
        return False

@login_required(login_url='/login/')
@permiso_requerido(permiso="Modificar item")
@miembro_proyecto()
@rol_fase_requerido()
@solicitud_requerida(accion="Modificar item")
def modificar_item_view(request, id_proyecto, id_fase, id_item):
    """
    ::
    
        La vista para modificar un item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Modificar item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario modificar un item de la fase previamente seleccionada, para lograr esto, 
        se verifica la validez de cada campo modificado y luego se guarda el item de acuerdo a los campos ingresados.
    
        La vista recibe los siguientes parametros:
    
            - request: contiene informacion sobre la sesion actual.
            - id_item: el identificador del item.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:    
        
            - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template de visualizacion del item modificado. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    item = fase.items.get(id=id_item)
    atributos = ValorAtributo.objects.filter(item__id=id_item)
    estado_valido = True
    item_valido = True
    existe_solicitud = True
    
    if fase.estado == 2:
        estado_valido = False
    
    if item.estado == 1 or item.estado == 2:
        item_valido = False
        
    try:
        solicitud = SolicitudCambio.objects.filter(item=item).get(accion="Modificar item")
    except SolicitudCambio.DoesNotExist:
        existe_solicitud = False
    
    form = ModificarItemForm()
    if estado_valido and item_valido or existe_solicitud:
        if request.method == "POST":
            form = ModificarItemForm(request.POST)
            if form.is_valid():
                nombre = form.cleaned_data['nombre']
                descripcion = form.cleaned_data['descripcion']
                complejidad = form.cleaned_data['complejidad']
                costo_monetario = form.cleaned_data['costo_monetario']
                costo_temporal = form.cleaned_data['costo_temporal']
                
                for a in atributos:
                    for key, value in request.POST.iteritems():
                        if a.tipo_atributo.nombre == key:
                            if a.tipo_atributo.tipo_dato == 0:
                                if is_number(value):
                                    a.valor_numerico = value
                                else:
                                    a.valor_numerico = None
                                a.save()
                            elif a.tipo_atributo.tipo_dato == 1:
                                if is_date(value):
                                    a.valor_fecha = value
                                else:
                                    a.valor_fecha = None
                                a.save()
                            elif a.tipo_atributo.tipo_dato == 2:
                                a.valor_texto_grande = value
                                a.save()
                            elif a.tipo_atributo.tipo_dato == 3:
                                a.valor_texto_chico = value
                                a.save()
                            elif a.tipo_atributo.tipo_dato == 4:
                                if value=="1":
                                    a.valor_logico = True
                                    a.save()
                                elif value=="0":
                                    a.valor_logico = False
                                    a.save()
                for a in atributos:
                    for key, value in request.FILES.iteritems():
                        if a.tipo_atributo.nombre == key:
                            if a.tipo_atributo.tipo_dato == 5:
                                a.valor_archivo = request.FILES[key]
                                a.save()
                
                if item.nombre != nombre or item.descripcion != descripcion or item.complejidad != complejidad or item.costo_monetario != costo_monetario or item.costo_temporal != costo_temporal:
                    item.version = VersionItem.objects.filter(id_item=item.id).latest('id').version + 1
                    item.nombre = nombre
                    item.descripcion = descripcion
                    item.complejidad = complejidad
                    item.costo_monetario = costo_monetario
                    item.costo_temporal = costo_temporal
                    item.save()
                    version_item = VersionItem.objects.create(version=item.version, id_item=item.id, nombre=item.nombre, 
                                                              descripcion=item.descripcion, costo_monetario=item.costo_monetario, 
                                                              costo_temporal=item.costo_temporal, complejidad=item.complejidad,
                                                              estado=item.estado, fase=item.fase, tipo_item=item.tipo_item,
                                                              adan=item.adan, cain=item.cain, tipo_relacion=item.tipo_relacion,
                                                              linea_base=item.linea_base, fecha_version=datetime.datetime.now())
                    if item.padre:
                        version_item.padre = item.padre.id
                    version_item.save()
                    
                # Si la solicitud de cambio correspondiente a la accion en cuestion existe.
                if existe_solicitud:
                    item.linea_base = solicitud.linea_base
                    item.estado = 2
                    item.save()
                    version_item.linea_base = item.linea_base
                    version_item.estado = item.estado
                    version_item.save()
                    # Borramos la solicitud de cambio que ya ha sido utilizada para efectuar los cambios en el item.
                    solicitud.delete()
                        
                return HttpResponseRedirect('/desarrollo/fases/items/item/%s/fase/%s/proyecto/%s'%(id_item, id_fase, id_proyecto))
    
    if request.method == "GET":
        form = ModificarItemForm(initial={
            'nombre': item.nombre,
            'descripcion': item.descripcion,
            'costo_temporal': item.costo_temporal,
            'costo_monetario': item.costo_monetario,
            'complejidad': item.complejidad,
            })
    ctx = {'form':form, 'item':item, 'fase':fase, 'proyecto':proyecto, 'atributos':atributos, 'setting':settings, 'estado_valido':estado_valido, 'item_valido':item_valido, 'existe_solicitud':existe_solicitud}
    return render_to_response('item/modificar_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Eliminar item")
@miembro_proyecto()
@rol_fase_requerido()
@solicitud_requerida(accion="Eliminar item")
def eliminar_item_view(request, id_proyecto, id_fase, id_item):
    """
    ::
    
        La vista para eliminar un item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Eliminar item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario eliminar un item de la fase previamente seleccionada, para lograr esto, 
        se verifica si el item cumple las siguientes condiciones:
        
            - El item debe estar en estado En construccion o En revision.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_item: el identificador del item.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o no se cumplieron las condiciones para eliminar, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de items por fase. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    item = Item.objects.get(id=id_item)
    atributos = ValorAtributo.objects.filter(item__id=id_item)
    relaciones = item.relaciones.all()
    estado_valido = True
    item_valido = True
    posee_relaciones = False
    existe_solicitud = True
    
    if fase.estado == 2:
        estado_valido = False
    
    if item.estado == 1 or item.estado == 2:
        item_valido = False
        
    if relaciones:
        posee_relaciones = True
        
    try:
        solicitud = SolicitudCambio.objects.filter(item=item).get(accion="Eliminar item")
    except SolicitudCambio.DoesNotExist:
        existe_solicitud = False
        
    if estado_valido and item_valido and posee_relaciones == False or existe_solicitud:
        if request.method == "POST":
            try:
                version_eliminada = VersionItem.objects.filter(id_item=item.id).get(version=item.version)
                version_eliminada.estado = 4
                version_eliminada.save()
            except VersionItem.DoesNotExist:
                pass
                    
            # Si la solicitud de cambio correspondiente a la accion en cuestion existe.
            if existe_solicitud:
                # Borramos la solicitud de cambio que ya ha sido utilizada para efectuar los cambios en el item.
                solicitud.delete()
                
            item.delete()
            return HttpResponseRedirect('/desarrollo/fases/items/fase/%s/proyecto/%s'%(id_fase, id_proyecto))
    
    ctx = {'item':item, 'fase':fase, 'proyecto':proyecto, 'atributos':atributos, 'setting':settings, 'estado_valido':estado_valido, 'item_valido':item_valido, 'posee_relaciones':posee_relaciones}
    return render_to_response('item/eliminar_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Visualizar item")
@miembro_proyecto()
@rol_fase_requerido()
def visualizar_item_view(request, id_proyecto, id_fase, id_item):
    """
    ::
    
        La vista para visualizar un item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Visualizar item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
    
        Esta vista permite al usuario visualizar todos los campos guardados de un item de la fase previamente seleccionada.
        La vista recibe los siguientes parametros:
    
            - request: contiene informacion sobre la sesion actual.
            - id_item: el identificador del item.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    item = fase.items.get(id=id_item)
    atributos = ValorAtributo.objects.filter(item__id=id_item)
    ctx = {'item':item, 'fase': fase, 'proyecto':proyecto, 'atributos':atributos, 'setting':settings}
    return render_to_response('item/visualizar_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Aprobar item")
@miembro_proyecto()
@rol_fase_requerido()
def aprobar_item_view(request, id_proyecto, id_fase, id_item):
    """
    ::
    
        La vista para aprobar un item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Aprobar item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
    
        Esta vista permite al usuario aprobar un item, es decir, cambiar el estado del item a Aprobado. Para lograr esto, el
        item debe estar en estado En Construccion o En Revision.
        La vista recibe los siguientes parametros:
    
            - request: contiene informacion sobre la sesion actual.
            - id_item: el identificador del item.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    item = fase.items.get(id=id_item)
    estado_valido = True
    item_valido = True
    
    if fase.estado == 2:
        estado_valido = False
    
    if item.estado == 1 or item.estado == 2:
        item_valido = False
        
    if estado_valido and item_valido:
        item.version = VersionItem.objects.filter(id_item=item.id).latest('id').version + 1
        item.estado = 1
        item.save()
        version_item = VersionItem.objects.create(version=item.version, id_item=item.id, nombre=item.nombre, 
                                                  descripcion=item.descripcion, costo_monetario=item.costo_monetario, 
                                                  costo_temporal=item.costo_temporal, complejidad=item.complejidad,
                                                  estado=item.estado, fase=item.fase, tipo_item=item.tipo_item,
                                                  adan=item.adan, cain=item.cain, tipo_relacion=item.tipo_relacion, 
                                                  linea_base=item.linea_base, fecha_version=datetime.datetime.now())
        if item.padre:
            version_item.padre = item.padre.id
        version_item.save()
        
    ctx = {'item':item, 'fase':fase, 'proyecto':proyecto, 'estado_valido':estado_valido, 'item_valido':item_valido}
    return render_to_response('item/aprobar_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@miembro_proyecto()
@rol_fase_requerido()
def desaprobar_item_view(request, id_proyecto, id_fase, id_item):
    """
    ::
    
        La vista para desaprobar un item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
    
        Esta vista permite al usuario desaprobar un item, es decir, cambiar el estado del item a En construccion. Para lograr esto, el
        item debe estar en estado Aprobado o Bloqueado.
        La vista recibe los siguientes parametros:
    
            - request: contiene informacion sobre la sesion actual.
            - id_item: el identificador del item.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    item = fase.items.get(id=id_item)
    estado_valido = True
    item_valido = True
    
    if fase.estado == 2:
        estado_valido = False
    
    if item.estado == 0 or item.estado == 2 or item.estado == 3:
        item_valido = False
        
    if estado_valido and item_valido:
        item.version = VersionItem.objects.filter(id_item=item.id).latest('id').version + 1
        item.estado = 0
        item.save()
        version_item = VersionItem.objects.create(version=item.version, id_item=item.id, nombre=item.nombre, 
                                                  descripcion=item.descripcion, costo_monetario=item.costo_monetario, 
                                                  costo_temporal=item.costo_temporal, complejidad=item.complejidad,
                                                  estado=item.estado, fase=item.fase, tipo_item=item.tipo_item,
                                                  adan=item.adan, cain=item.cain, tipo_relacion=item.tipo_relacion, 
                                                  linea_base=item.linea_base, fecha_version=datetime.datetime.now())
        if item.padre:
            version_item.padre = item.padre.id
        version_item.save()
        
    ctx = {'item':item, 'fase':fase, 'proyecto':proyecto, 'estado_valido':estado_valido, 'item_valido':item_valido}
    return render_to_response('item/desaprobar_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@miembro_proyecto()
@rol_fase_requerido()
def calcular_impacto_view(request, id_proyecto, id_fase, id_item):
    """
    ::
    
        La vista para calcular impacto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            - El usuario debe poseer un rol valido para la fase.
    
        Esta vista permite al usuario visualizar el calculo de impacto monetario y temporal de un item.
        La vista recibe los siguientes parametros:
    
            - request: contiene informacion sobre la sesion actual.
            - id_item: el identificador del item.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    item = fase.items.get(id=id_item)
    relaciones = item.relaciones.all()
    costo_monetario = item.costo_monetario
    costo_temporal = item.costo_temporal
    posee_hijos = False
    
    # Verificamos si el item de la solicitud de cambio posee hijos/sucesores.
    if relaciones:
        posee_hijos = True
        
    if posee_hijos:
        # Cargamos en el listado hijos todos los hijos/sucesores del item de la solicitud de cambio.
        hijos = []
                            
        # Obtenemos todos los hijos/sucesores del item.
        while 1:
            nuevas_relaciones = []
            if len(relaciones) == 0:
                break
            for r in relaciones:
                hijos.append(r)
                if r.relaciones.count() > 0:
                    for h in r.relaciones.all():
                        nuevas_relaciones.append(h)
                relaciones = nuevas_relaciones
    
        # Calculamos el costo de impacto monetario y temporal del item de la solicitud.
        for h in hijos:
            costo_monetario = costo_monetario + h.costo_monetario
            costo_temporal = costo_temporal + h.costo_temporal
    
    # Creamos el grafo de relaciones del item de la solicitud de cambio.
    fases = proyecto.fases.all()
    grafo_relaciones = pydot.Dot(graph_type='digraph', fontname="Verdana", rankdir="TB")
    grafo_relaciones.set_node_defaults(style="filled", fillcolor="white", shape="record")
    grafo_relaciones.set_edge_defaults(color="black", arrowhead="vee")
    
    for f in fases:
        cluster_fase = pydot.Cluster("fase"+str(f.id),
                                     label="Fase: " + str(f.nombre), 
                                     shape='rectangle', 
                                     fontsize=15, 
                                     style='filled', 
                                     color='#E6E6E6', 
                                     fillcolor="#BDBDBD", 
                                     fontcolor="white")
        items = f.items.exclude(estado=2).filter(linea_base=None)
        if items:
            for i in items:
                if i == item:
                    color_estado = "white"
                    if i.estado == 1:
                        color_estado = "#80FF00"
                    elif i.estado == 3:
                        color_estado = "#045FB4"
                    
                    cluster_fase.add_node(pydot.Node("item"+str(i.id),
                                          label = "<f0>Item: %s|<f1>Costo: %d"%(i.nombre, i.costo_monetario),
                                          fillcolor=color_estado, 
                                          fontsize=15))
                if posee_hijos:
                    if i in hijos:
                        color_estado = "white"
                        if i.estado == 1:
                            color_estado = "#80FF00"
                        elif i.estado == 3:
                            color_estado = "#045FB4"
                        
                        cluster_fase.add_node(pydot.Node("item"+str(i.id),
                                              label = "<f0>Item: %s|<f1>Costo: %d"%(i.nombre, i.costo_monetario),
                                              fillcolor=color_estado, 
                                              fontsize=15))
                
        items = f.items.exclude(linea_base=None)
        if items:
            lineas_base = f.lineas_base.all().exclude(estado=2)
            for lb in lineas_base:
                cluster_linea_base = pydot.Cluster("lb"+str(lb.id), 
                                                   label="Linea base: " + str(lb.nombre), 
                                                   shape='rectangle', 
                                                   fontsize=15, 
                                                   style='filled', 
                                                   color='#E6E6E6', 
                                                   fillcolor="#FFFFFF", 
                                                   fontcolor="black")
                items = lb.items.all()
                for i in items:
                    if i == item:
                        if i.estado == 1:
                            color_estado = "#80FF00"
                        elif i.estado == 2:
                            color_estado = "#DF0101"
                        else:
                            color_estado = "#045FB4"
                        
                        cluster_linea_base.add_node(pydot.Node("item"+str(i.id), 
                                                               label = "<f0>Item: %s|<f1>Costo: %d"%(i.nombre, i.costo_monetario), 
                                                               fillcolor=color_estado, 
                                                               fontsize=15))
                        
                    if posee_hijos:
                        if i in hijos:
                            if i.estado == 1:
                                color_estado = "#80FF00"
                            elif i.estado == 2:
                                color_estado = "#DF0101"
                            else:
                                color_estado = "#045FB4"
                            
                            cluster_linea_base.add_node(pydot.Node("item"+str(i.id), 
                                                                   label = "<f0>Item: %s|<f1>Costo: %d"%(i.nombre, i.costo_monetario), 
                                                                   fillcolor=color_estado, 
                                                                   fontsize=15))
                cluster_fase.add_subgraph(cluster_linea_base)
            
        grafo_relaciones.add_subgraph(cluster_fase)

    for f in fases:
        items = f.items.all()
        for i in items:
            if i == item:
                relaciones = i.relaciones.all()
                for r in relaciones:
                    grafo_relaciones.add_edge(pydot.Edge("item"+str(i.id), "item"+str(r.id), 
                                                       label='costo='+str(i.costo_monetario), 
                                                       fontsize=10))
            if posee_hijos:
                if i in hijos:
                    relaciones = i.relaciones.all()
                    for r in relaciones:
                        grafo_relaciones.add_edge(pydot.Edge("item"+str(i.id), "item"+str(r.id), 
                                                           label='costo='+str(i.costo_monetario), 
                                                           fontsize=10))
    # La direccion del grafico png que representa al grafo de relaciones del item de la solicitud de cambio.
    ruta_grafo = str(settings.MEDIA_ROOT) + "grafos/grafo_relaciones_item_" + str(item.nombre) + ".png"
    grafo_relaciones.write(ruta_grafo, prog='dot', format='png')
    ruta_grafo = str(settings.MEDIA_URL) + "grafos/grafo_relaciones_item_" + str(item.nombre) + ".png"
            
    ctx = {'item':item, 'fase':fase, 'proyecto':proyecto, 'ruta_grafo':ruta_grafo, 'posee_hijos':posee_hijos, 'costo_monetario':costo_monetario, 'costo_temporal':costo_temporal}
    return render_to_response('item/calculo_impacto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@miembro_proyecto()
@rol_fase_requerido()
def revivir_item_view(request, id_proyecto, id_fase):
    """
    ::
    
        La vista para revivir un item eliminado. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Revivir item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario ver un listado de todos los items previamente eliminados de la fase actual. En el template 
        generado se tendra la opcion de revivir los items del listado otorgado.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    items_eliminados = VersionItem.objects.filter(fase=fase).filter(estado=4)
    estado_valido = True
    
    if fase.estado == 2:
        estado_valido = False
    
    ctx = {"items_eliminados":items_eliminados, "fase":fase, "proyecto":proyecto, 'estado_valido':estado_valido}
    return render_to_response('item/items_eliminados.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Revivir item")
@miembro_proyecto()
@rol_fase_requerido()
def confirmacion_revivir_item_view(request, id_proyecto, id_fase, id_item):
    """
    ::
    
        La vista para revivir un item eliminado. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Revivir item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario revivir un item previamente eliminado. Se encarga de revisar si el item a revivir 
        quiere entrar en una fase en estado Finalizado, en cuyo caso, se abortara la operacion. Ademas, verifica si el
        item a revivir poseia un padre. Si tenia un padre, la vista se encarga de reasignar el item a la lista de 
        hijos/sucesores del padre item. Si no poseia padre, simplemente queda sin padre; los usuarios estan a cargo de 
        asignarlo a un padre item si se necesitase.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_item: el identificador del item.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente.  
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    item = VersionItem.objects.filter(id_item=id_item).get(estado=4)
    estado_valido = True
    posee_padre = False
    
    if fase.estado == 2:
        estado_valido = False
    
    if item.padre:
        posee_padre = True
    
    if posee_padre:
        
        existe_padre = True
        try:
            item_padre = fase.items.get(id=item.padre)
        except Item.DoesNotExist:
            existe_padre = False
            
            if estado_valido:
                item_revivido = Item.objects.create(id=item.id_item, nombre=item.nombre, version=item.version, estado=0, 
                                                    descripcion=item.descripcion, costo_monetario=item.costo_monetario, 
                                                    costo_temporal=item.costo_temporal, complejidad=item.complejidad,
                                                    linea_base=item.linea_base, fase=item.fase, tipo_item=item.tipo_item)
                item_revivido.save()
                item.estado = 0
                item.save()
                
                tipo_item = TipoItem.objects.get(id=item.tipo_item.id)
                tipos_atributo = tipo_item.tipos_atributo.all()
                for tipo_atributo in tipos_atributo:
                    valor_atributo = ValorAtributo.objects.create(item=item_revivido, tipo_item=tipo_item, tipo_atributo=tipo_atributo)
                    valor_atributo.save()
                
                ctx = {"item_revivido":item_revivido, "fase":fase, "proyecto":proyecto, "posee_padre":posee_padre, "existe_padre":existe_padre, "estado_valido":estado_valido}
                return render_to_response('item/confirmacion_revivir_item.html', ctx, context_instance=RequestContext(request))
            else:
                ctx = {"item":item, "fase":fase, "proyecto":proyecto, "estado_valido":estado_valido, "posee_padre":posee_padre}
                return render_to_response('item/confirmacion_revivir_item.html', ctx, context_instance=RequestContext(request))
            
        if estado_valido:
            item_revivido = Item.objects.create(id=item.id_item, nombre=item.nombre, version=item.version, estado=0, 
                                                descripcion=item.descripcion, costo_monetario=item.costo_monetario, 
                                                costo_temporal=item.costo_temporal, complejidad=item.complejidad,
                                                fase=item.fase, tipo_item=item.tipo_item, adan=item.adan,
                                                cain=item.cain, padre=item_padre, tipo_relacion=item.tipo_relacion,
                                                linea_base=item.linea_base)
            if item_padre.adan:
                item_revivido.adan = item_padre.adan
            else:
                item_revivido.adan = item_padre.id
            if item_padre.adan and item_padre.cain == None:
                item_revivido.adan = item_padre.adan
                item_revivido.cain = item_padre.id
            elif item_padre.adan and item_padre.cain:
                item_revivido.cain = item_padre.cain
            item_revivido.save()
            
            item.estado = 0
            item.save()
            
            tipo_item = TipoItem.objects.get(id=item.tipo_item.id)
            tipos_atributo = tipo_item.tipos_atributo.all()
            for tipo_atributo in tipos_atributo:
                valor_atributo = ValorAtributo.objects.create(item=item_revivido, tipo_item=tipo_item, tipo_atributo=tipo_atributo)
                valor_atributo.save()
            
            item_padre.relaciones.add(item_revivido)
            item_padre.save()
            
            ctx = {"item_revivido":item_revivido, "item_padre":item_padre, "fase":fase, "proyecto":proyecto, "existe_padre":existe_padre, "estado_valido":estado_valido, "posee_padre":posee_padre}
            return render_to_response('item/confirmacion_revivir_item.html', ctx, context_instance=RequestContext(request))
        else:
            ctx = {"item":item, "fase":fase, "proyecto":proyecto, "estado_valido":estado_valido, "posee_padre":posee_padre}
            return render_to_response('item/confirmacion_revivir_item.html', ctx, context_instance=RequestContext(request))
    else:
        if estado_valido:
            item_revivido = Item.objects.create(id=item.id_item, nombre=item.nombre, version=item.version, estado=0, 
                                                descripcion=item.descripcion, costo_monetario=item.costo_monetario, 
                                                costo_temporal=item.costo_temporal, complejidad=item.complejidad,
                                                fase=item.fase, tipo_item=item.tipo_item, linea_base=item.linea_base)
            item_revivido.save()
            item.estado = 0
            item.save()
            
            tipo_item = TipoItem.objects.get(id=item.tipo_item.id)
            tipos_atributo = tipo_item.tipos_atributo.all()
            for tipo_atributo in tipos_atributo:
                valor_atributo = ValorAtributo.objects.create(item=item_revivido, tipo_item=tipo_item, tipo_atributo=tipo_atributo)
                valor_atributo.save()
            
            ctx = {"item_revivido":item_revivido, "fase":fase, "proyecto":proyecto, "posee_padre":posee_padre, "estado_valido":estado_valido}
            return render_to_response('item/confirmacion_revivir_item.html', ctx, context_instance=RequestContext(request))
        else:
            ctx = {"item":item, "fase":fase, "proyecto":proyecto, "posee_padre":posee_padre, "estado_valido":estado_valido}
            return render_to_response('item/confirmacion_revivir_item.html', ctx, context_instance=RequestContext(request))
            
@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar relaciones de item")
@miembro_proyecto()
@rol_fase_requerido()
def relaciones_item_view(request, id_proyecto, id_fase, id_item):
    """
    ::
    
        La vista del listado de relaciones por item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Gestionar relaciones de item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario listar y conocer las opciones de las relaciones del item seleccionado.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_item: el identificador del item.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    item = fase.items.get(id=id_item)
    padre = item.padre 
    hijos = item.relaciones.all()
    ctx = {'item':item, 'padre':padre, 'hijos':hijos, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('item/relaciones_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@miembro_proyecto()
@rol_fase_requerido()
def agregar_relacion_view(request, id_proyecto, id_fase, id_item):
    """
    ::
    
        La vista del listado de items pertenecientes a la fase siguiente o la misma fase. La eleccion de una de las anteriores dependera
        del tipo de relacion que se quiera agregar (Padre-Hijo o Antecesor-Sucesor). Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_item: el identificador del item.
            - id_fase: el identificador del la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    item = fase.items.get(id=id_item)
        
    if request.method == "POST":
        eleccion_relacion = request.POST.get('eleccion_relacion')
            
        # Hijos para el item padre
        if eleccion_relacion == "0":
            existen_items_hijos = False
            items_hijos = fase.items.filter(padre=None).exclude(id=id_item).exclude(estado=1).exclude(estado=2)
                
            if item.adan:
                items_hijos = items_hijos.exclude(id=item.adan)
            if item.cain:
                items_hijos = items_hijos.exclude(id=item.cain)
                
            if items_hijos:
                existen_items_hijos = True
                
            ctx = {'item':item, 'items_hijos':items_hijos, 'fase':fase, 'proyecto':proyecto, 'existen_items_hijos':existen_items_hijos, 'eleccion':eleccion_relacion}
            return render_to_response('item/agregar_relacion.html', ctx, context_instance=RequestContext(request))
            
        # Sucesores para el item antecesor
        elif eleccion_relacion == "1":
            estado_item_valido = False
            secuencia_fase_valida = True
                
            if item.estado == 2:
                estado_item_valido = True
                
            cant_secuencias = proyecto.fases.count() 
            if fase.num_secuencia == cant_secuencias:
                secuencia_fase_valida = False
                
            if secuencia_fase_valida and estado_item_valido:
                existen_items_sucesores = False
                fase_vecina = proyecto.fases.get(num_secuencia=int(fase.num_secuencia)+1)
                items_sucesores = fase_vecina.items.filter(padre=None).exclude(estado=1).exclude(estado=2)
                    
                if items_sucesores:
                    existen_items_sucesores = True
                    
                ctx = {'item':item, 'fase':fase, 'proyecto':proyecto, 'fase_vecina':fase_vecina, 'items_sucesores':items_sucesores, 'estado_item_valido':estado_item_valido, 'secuencia_fase_valida':secuencia_fase_valida, 'existen_items_sucesores':existen_items_sucesores, 'eleccion':eleccion_relacion}
                return render_to_response('item/agregar_relacion.html', ctx, context_instance=RequestContext(request))
            else:
                ctx = {'item':item, 'fase':fase, 'proyecto':proyecto, 'estado_item_valido':estado_item_valido, 'secuencia_fase_valida':secuencia_fase_valida, 'eleccion':eleccion_relacion}
                return render_to_response('item/agregar_relacion.html', ctx, context_instance=RequestContext(request))
                    
        # Padres para el item hijo
        elif eleccion_relacion == "2":
            posee_padre = False
            existen_items_padres = False
            items_padres = fase.items.exclude(id=item.id).exclude(adan=item.id)
                
            if item.padre:
                posee_padre = True
                    
            if items_padres:
                existen_items_padres = True
                    
            ctx = {'item':item, 'items_padres':items_padres, 'fase':fase, 'proyecto':proyecto, 'existen_items_padres':existen_items_padres, 'posee_padre':posee_padre, 'eleccion':eleccion_relacion}
            return render_to_response('item/agregar_relacion.html', ctx, context_instance=RequestContext(request))
            
        # Antecesores para el item sucesor
        elif eleccion_relacion == "3":
            posee_padre = False
            secuencia_fase_valida = True
                
            if item.padre:
                posee_padre = True
                     
            if fase.num_secuencia == 1:
                secuencia_fase_valida = False
                    
            if posee_padre == False and secuencia_fase_valida:
                existen_items_antecesores = False
                fase_vecina = proyecto.fases.get(num_secuencia=int(fase.num_secuencia)-1)
                items_antecesores = fase_vecina.items.filter(estado=2)
                    
                if items_antecesores:
                    existen_items_antecesores = True
                        
                ctx = {'item':item, 'fase':fase, 'proyecto':proyecto, 'fase_vecina':fase_vecina, 'items_antecesores':items_antecesores, 'secuencia_fase_valida':secuencia_fase_valida, 'existen_items_antecesores':existen_items_antecesores, 'posee_padre':posee_padre, 'eleccion':eleccion_relacion}
                return render_to_response('item/agregar_relacion.html', ctx, context_instance=RequestContext(request))
            else:
                ctx = {'item':item, 'fase':fase, 'proyecto':proyecto, 'secuencia_fase_valida':secuencia_fase_valida, 'posee_padre':posee_padre, 'eleccion':eleccion_relacion}
                return render_to_response('item/agregar_relacion.html', ctx, context_instance=RequestContext(request))
            
    ctx = {'item':item, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('item/agregar_relacion.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar relacion a item")
@miembro_proyecto()
@rol_fase_requerido()
@solicitud_requerida(accion="Agregar relacion a item")
def confirmacion_agregar_relacion_view(request, id_proyecto, id_fase, id_item, id_relacion, eleccion):
    """
    ::
    
        La vista de la confirmacion de agregacion de una relacion a un item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Agregar relacion a item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
        
        Esta funcionalidad se encarga de realizar la agregacion de relacion. No posee excepciones, puesto que, los items a seleccionar para
        la agregacion cumplen con todos los requisitos necesarios para evitar inconsistencias en el grafo de items relacionados.
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_item: el identificador del item.
            - id_fase: el identificador del la fase.
            - id_relacion: el identificador del item a relacionar.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    estado_valido = True
    item_valido = True
    existe_solicitud = True
    
    if fase.estado == 2:
        estado_valido = False
    
    if eleccion == "0" or eleccion == "1":
        item = fase.items.get(id=id_item)
        relacion = Item.objects.get(id=id_relacion)
        
        try:
            solicitud = SolicitudCambio.objects.filter(item=item).get(accion="Agregar relacion a item")
        except SolicitudCambio.DoesNotExist:
            existe_solicitud = False
        
        if item.estado == 1 or item.estado == 2:
            item_valido = False
        
    elif eleccion == "2" or eleccion == "3" :
        relacion = fase.items.get(id=id_item)
        item = Item.objects.get(id=id_relacion)
        
        try:
            solicitud = SolicitudCambio.objects.filter(item=relacion).get(accion="Agregar relacion a item")
        except SolicitudCambio.DoesNotExist:
            existe_solicitud = False
        
        if relacion.estado == 1 or relacion.estado == 2:
            item_valido = False
    
    if estado_valido and item_valido or existe_solicitud:
        if item.fase.id == relacion.fase.id:
            relacion.tipo_relacion = 0
        else:
            relacion.tipo_relacion = 1
        relacion.save()
            
        # Si el padre del item a relacionar es adan.
        if item.adan == None:
            relacion.adan = item.id
            relacion.cain = None
            relacion.padre = item
            relacion.version = VersionItem.objects.filter(id_item=relacion.id).latest('id').version + 1
            relacion.save()
                        
            # Version del item guardada.
            version_relacion = VersionItem.objects.create(version=relacion.version, id_item=relacion.id, nombre=relacion.nombre, 
                                                          descripcion=relacion.descripcion, costo_monetario=relacion.costo_monetario, 
                                                          costo_temporal=relacion.costo_temporal, complejidad=relacion.complejidad,
                                                          estado=relacion.estado, fase=relacion.fase, tipo_item=relacion.tipo_item,
                                                          adan=relacion.adan, cain=relacion.cain, tipo_relacion=relacion.tipo_relacion, 
                                                          linea_base=relacion.linea_base, fecha_version=datetime.datetime.now())
            if relacion.padre:
                version_relacion.padre = relacion.padre.id
            version_relacion.save()
                    
            # Verificamos si existen items que son hijos/sucesores del item a relacionar.
            relaciones = relacion.relaciones.all()
            # Si existe al menos uno, se cargaran todos los hijos/sucesores en la lista resultados.
            if relaciones:
                resultados = []
                            
                while 1:
                    nuevas_relaciones = []
                    if len(relaciones) == 0:
                        break
                    for r in relaciones:
                        resultados.append(r)
                        if r.relaciones.count() > 0:
                            for h in r.relaciones.all():
                                nuevas_relaciones.append(h)
                    relaciones = nuevas_relaciones
                            
                # Por cada hijo/sucesor se modificaran sus campos de gestion de cosistencia del grafo.
                for r in resultados:
                    r.adan = relacion.padre.id
                    r.cain = relacion.id
                    r.version = VersionItem.objects.filter(id_item=r.id).latest('id').version + 1
                    r.save()
                                
                    version_r = VersionItem.objects.create(version=r.version, id_item=r.id, nombre=r.nombre, 
                                                           descripcion=r.descripcion, costo_monetario=r.costo_monetario, 
                                                           costo_temporal=r.costo_temporal, complejidad=r.complejidad,
                                                           estado=r.estado, fase=r.fase, tipo_item=r.tipo_item,
                                                           adan=r.adan, cain=r.cain, tipo_relacion=r.tipo_relacion, 
                                                           linea_base=r.linea_base, fecha_version=datetime.datetime.now())
                    if r.padre:
                        version_r.padre = r.padre.id
                    version_r.save()
        # Fin--> Si el padre del item a relacionar es adan.
        # Si el padre del item a relacionar no es adan.
        else:
            relacion.adan = item.adan
            relacion.cain = item.id
            relacion.padre = item
            relacion.version = VersionItem.objects.filter(id_item=relacion.id).latest('id').version + 1
            relacion.save()
                        
            # Version del item guardada.
            version_relacion = VersionItem.objects.create(version=relacion.version, id_item=relacion.id, nombre=relacion.nombre, 
                                                          descripcion=relacion.descripcion, costo_monetario=relacion.costo_monetario, 
                                                          costo_temporal=relacion.costo_temporal, complejidad=relacion.complejidad,
                                                          estado=relacion.estado, fase=relacion.fase, tipo_item=relacion.tipo_item,
                                                          adan=relacion.adan, cain=relacion.cain, tipo_relacion=relacion.tipo_relacion, 
                                                          linea_base=relacion.linea_base, fecha_version=datetime.datetime.now())
            if relacion.padre:
                version_relacion.padre = relacion.padre.id
            version_relacion.save()
                        
            # Verificamos si existen items que son hijos/sucesores del item a relacionar.
            relaciones = relacion.relaciones.all()
            # Si existe al menos uno, se cargaran todos los hijos/sucesores en la lista resultados.
            if relaciones:
                resultados = []
                            
                while 1:
                    nuevas_relaciones = []
                    if len(relaciones) == 0:
                        break
                    for r in relaciones:
                        resultados.append(r)
                        if r.relaciones.count() > 0:
                            for h in r.relaciones.all():
                                nuevas_relaciones.append(h)
                    relaciones = nuevas_relaciones
                            
                # Por cada hijo/sucesor se modificaran sus campos de gestion de cosistencia del grafo.
                for r in resultados:
                    r.adan = relacion.padre.id
                    r.cain = relacion.id
                    r.version = VersionItem.objects.filter(id_item=r.id).latest('id').version + 1
                    r.save()
                                
                    version_r = VersionItem.objects.create(version=r.version, id_item=r.id, nombre=r.nombre, 
                                                           descripcion=r.descripcion, costo_monetario=r.costo_monetario, 
                                                           costo_temporal=r.costo_temporal, complejidad=r.complejidad,
                                                           estado=r.estado, fase=r.fase, tipo_item=r.tipo_item,
                                                           adan=r.adan, cain=r.cain, tipo_relacion=r.tipo_relacion, 
                                                           linea_base=r.linea_base, fecha_version=datetime.datetime.now())
                    if r.padre:
                        version_r.padre = r.padre.id
                    version_r.save()
        # Fin--> Si el padre del item a relacionar no es adan.
            
        item.relaciones.add(relacion)
        item.save()
        
    # Si la solicitud de cambio correspondiente a la accion en cuestion existe.
    if existe_solicitud:
        if eleccion == "0" or eleccion == "1":
            item.linea_base = solicitud.linea_base
            item.estado = 2
            item.save()
            version_item = VersionItem.objects.filter(id_item=item.id).latest('id')
            version_item.linea_base = item.linea_base
            version_item.estado = item.estado
            version_item.save()
        elif eleccion == "2" or eleccion == "3" :
            relacion.linea_base = solicitud.linea_base
            relacion.estado = 2
            relacion.save()
            version_relacion = VersionItem.objects.filter(id_item=relacion.id).latest('id')
            version_relacion.linea_base = relacion.linea_base
            version_relacion.estado = relacion.estado
            version_relacion.save()
        # Borramos la solicitud de cambio que ya ha sido utilizada para efectuar los cambios en el item.
        solicitud.delete()

    ctx = {'item':item, 'relacion':relacion, 'fase':fase, 'proyecto':proyecto, 'eleccion':eleccion, 'estado_valido':estado_valido, 'item_valido':item_valido, 'existe_solicitud':existe_solicitud}
    return render_to_response('item/confirmacion_agregar_relacion.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Quitar relacion de item")
@miembro_proyecto()
@rol_fase_requerido()
@solicitud_requerida(accion="Quitar relacion de item")
def quitar_relacion_view(request, id_proyecto, id_fase, id_item, id_relacion, eleccion):
    """
    ::
    
        La vista para quitar una relacion de un item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Quitar relacion de item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
        
        Esta funcionalidad permite a un usuario romper una relacion entre el padre/antecesor item y un hijo hijo/sucesor. Ademas de esto, 
        todos aquellos items hijos/sucesores del item hijo/sucesor en cuestion pasan a cambiar el valor de su padre raiz por el identificador
        del item hijo/sucesor en cuestion.
            - request: contiene informacion sobre la sesion actual.
            - id_item: el identificador del item.
            - id_fase: el identificador del la fase.
            - id_relacion: el identificador del item a relacionar.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    estado_valido = True
    item_valido = True
    existe_solicitud = True
    
    if fase.estado == 2:
        estado_valido = False
    
    if eleccion == "0" or eleccion == "1":
        item = fase.items.get(id=id_item)
        relacion = Item.objects.get(id=id_relacion)
        
        try:
            solicitud = SolicitudCambio.objects.filter(item=item).get(accion="Quitar relacion de item")
        except SolicitudCambio.DoesNotExist:
            existe_solicitud = False
        
        if item.estado == 1 or item.estado == 2:
            item_valido = False
    elif eleccion == "2" or eleccion == "3" :
        item = Item.objects.get(id=id_item)
        relacion = fase.items.get(id=id_relacion)
        
        try:
            solicitud = SolicitudCambio.objects.filter(item=relacion).get(accion="Quitar relacion de item")
        except SolicitudCambio.DoesNotExist:
            existe_solicitud = False
        
        if relacion.estado == 1 or relacion.estado == 2:
            item_valido = False

    if estado_valido and item_valido or existe_solicitud:
        relacion.adan = None
        relacion.cain = None
        relacion.padre = None
        relacion.tipo_relacion = None
        relacion.version = VersionItem.objects.filter(id_item=relacion.id).latest('id').version + 1
        relacion.save()
        version_relacion = VersionItem.objects.create(version=relacion.version, id_item=relacion.id, nombre=relacion.nombre, 
                                                      descripcion=relacion.descripcion, costo_monetario=relacion.costo_monetario, 
                                                      costo_temporal=relacion.costo_temporal, complejidad=relacion.complejidad,
                                                      estado=relacion.estado, fase=relacion.fase, tipo_item=relacion.tipo_item,
                                                      adan=relacion.adan, cain=relacion.cain, tipo_relacion=relacion.tipo_relacion, 
                                                      linea_base=relacion.linea_base, fecha_version=datetime.datetime.now())
        if relacion.padre:
            version_relacion.padre = relacion.padre.id
        version_relacion.save()
        
        relaciones = relacion.relaciones.all()
        for r in relaciones:
            r.adan = relacion.id
            r.cain = None
            r.version = VersionItem.objects.filter(id_item=r.id).latest('id').version + 1
            r.save()
            version_r = VersionItem.objects.create(version=r.version, id_item=r.id, nombre=r.nombre, 
                                                   descripcion=r.descripcion, costo_monetario=r.costo_monetario, 
                                                   costo_temporal=r.costo_temporal, complejidad=r.complejidad,
                                                   estado=r.estado, fase=r.fase, tipo_item=r.tipo_item,
                                                   adan=r.adan, cain=r.cain, tipo_relacion=r.tipo_relacion, 
                                                   linea_base=r.linea_base, fecha_version=datetime.datetime.now())
            if r.padre:
                version_r.padre = r.padre.id
            version_r.save()
            
            hijos = r.relaciones.all()
            resultados = []
            
            while 1:
                nuevas_relaciones = []
                if len(hijos) == 0:
                    break
                for h in hijos:
                    resultados.append(h)
                    if h.relaciones.count() > 0:
                        for s in h.relaciones.all():
                            nuevas_relaciones.append(s)
                hijos = nuevas_relaciones
            
            for h in resultados:
                h.adan = relacion.id
                h.cain = r.id
                h.version = VersionItem.objects.filter(id_item=h.id).latest('id').version + 1
                h.save()
                version_h = VersionItem.objects.create(version=h.version, id_item=h.id, nombre=h.nombre, 
                                                       descripcion=h.descripcion, costo_monetario=h.costo_monetario, 
                                                       costo_temporal=h.costo_temporal, complejidad=h.complejidad,
                                                       estado=h.estado, fase=h.fase, tipo_item=h.tipo_item,
                                                       adan=h.adan, cain=h.cain, tipo_relacion=h.tipo_relacion, 
                                                       linea_base=h.linea_base, fecha_version=datetime.datetime.now())
                if h.padre:
                    version_h.padre = h.padre.id
                version_h.save()
            
    # Si la solicitud de cambio correspondiente a la accion en cuestion existe.
    if existe_solicitud:
        if eleccion == "0" or eleccion == "1":
            item.linea_base = solicitud.linea_base
            item.estado = 2
            item.save()
            version_item = VersionItem.objects.filter(id_item=item.id).latest('id')
            version_item.linea_base = item.linea_base
            version_item.estado = item.estado
            version_item.save()
        elif eleccion == "2" or eleccion == "3" :
            relacion.linea_base = solicitud.linea_base
            relacion.estado = 2
            relacion.save()
            version_relacion = VersionItem.objects.filter(id_item=relacion.id).latest('id')
            version_relacion.linea_base = relacion.linea_base
            version_relacion.estado = relacion.estado
            version_relacion.save()
        # Borramos la solicitud de cambio que ya ha sido utilizada para efectuar los cambios en el item.
        solicitud.delete()
            
    ctx = {'item':item, 'relacion':relacion, 'fase':fase, 'proyecto':proyecto, 'eleccion':eleccion, 'estado_valido':estado_valido, 'item_valido':item_valido, 'existe_solicitud':existe_solicitud}
    return render_to_response('item/quitar_relacion.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar versiones de item")
@miembro_proyecto()
@rol_fase_requerido()
def versiones_item_view(request, id_proyecto, id_fase, id_item):
    """
    ::
    
        La vista del listado de versiones por item. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Gestionar versiones de item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario listar las versiones de un item previamente seleccionado. Por cada item en la tabla de 
        versiones, se podra reversionar uno eligido.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_item: el identificador del item.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    item = fase.items.get(id=id_item)
    versiones = VersionItem.objects.filter(id_item=id_item).exclude(estado=4).exclude(version=item.version)
    ctx = {'item':item, 'versiones':versiones, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('item/versiones_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Reversionar item")
@miembro_proyecto()
@rol_fase_requerido()
@solicitud_requerida(accion="Reversionar item")
def confirmacion_reversionar_item_view(request, id_proyecto, id_fase, id_item, id_reversion):
    """
    ::
    
        La vista de la confirmacion de reversionado de un item previamente seleccionado. Para acceder a esta vista se deben cumplir los 
        siguientes requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Reversionar item.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
        
        Esta funcionalidad se encarga de realizar el reversionado de item. Se verifica si el item a reversionar no provoca inconsistencias en el 
        grafo de relaciones del proyecto.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_item: el identificador del item.
            - id_fase: el identificador del la fase.
            - id_reversion: el identificador del item reversionado.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    item = fase.items.get(id=id_item)
    item_reversion = VersionItem.objects.get(id=id_reversion)
    estado_valido = True
    fase_valida = True
    posee_hijos = False
    
    if item.estado == 1 or item.estado == 2:
        estado_valido = False
    
    if fase.estado == 2:
        fase_valida = False
        
    if item.relaciones.all():
        posee_hijos = True
    
    # Si el estado del item a reemplazar con la reversion no es Aprobado ni Bloqueado, el estado de la fase no es Finalizado y el item a reversionar no posee hijos/sucesores.
    if estado_valido and fase_valida and posee_hijos == False:
        posee_padre = False
        
        if item_reversion.padre:
            posee_padre = True
            
        # Si el item a reversionar posee un padre/antecesor.
        if posee_padre:
            existe_padre = True
            estado_padre_valido = True
            
            try:
                item_padre = Item.objects.get(id=item_reversion.padre)
                if item_padre.fase.id != item_reversion.fase.id:
                    if item_padre.estado != 2:
                        estado_padre_valido = False
            except Item.DoesNotExist:
                existe_padre = False
            
            # Si el padre (del item a reversionar) existe y ademas posee un estado valido.
            if existe_padre and estado_padre_valido:
                item.nombre = item_reversion.nombre
                item.version = item_reversion.version
                item.estado = item_reversion.estado
                item.descripcion = item_reversion.descripcion
                item.costo_monetario = item_reversion.costo_monetario
                item.costo_temporal = item_reversion.costo_temporal
                item.complejidad = item_reversion.complejidad
                item.fase = item_reversion.fase
                item.tipo_item = item_reversion.tipo_item
                item.linea_base = item_reversion.linea_base
                
                # Verificamos si el padre y el item a reversionar pertenecen a la misma fase.
                if item_padre.fase == item.fase:
                    item.tipo_relacion = 0
                else:
                    item.tipo_relacion = 1
                
                # Si el padre del item a reversionar es adan.
                if item_padre.adan == None:
                    item.adan = item_padre.id
                    item.cain = None
                    item.padre = item_padre
                    item.save()
                # Fin--> Si el padre del item a reversionar es adan.
                # Si el padre del item a reversionar no es adan.
                elif item_padre.adan:
                    item.adan = item_padre.adan
                    item.cain = item_padre.id
                    item.padre = item_padre
                    item.save()
                # Fin--> Si el padre del item a reversionar no es adan.
                
                ctx = {"item_reversion":item_reversion, "item":item, "fase":fase, "proyecto":proyecto, "posee_padre":posee_padre, "existe_padre":existe_padre, "estado_padre_valido":estado_padre_valido, "estado_valido":estado_valido, "fase_valida":fase_valida, 'posee_hijos':posee_hijos}
                return render_to_response('item/confirmacion_reversionar_item.html', ctx, context_instance=RequestContext(request))
            # Fin--> Si el padre (del item a reversionar) existe y ademas posee un estado valido.
            # Si el padre (del item a reversionar) no existe o el padre posee un estado no valido.
            else:
                item.nombre = item_reversion.nombre
                item.version = VersionItem.objects.filter(id_item=item.id).latest('id').version + 1
                item.estado = item_reversion.estado
                item.descripcion = item_reversion.descripcion
                item.costo_monetario = item_reversion.costo_monetario
                item.costo_temporal = item_reversion.costo_temporal
                item.complejidad = item_reversion.complejidad
                item.fase = item_reversion.fase
                item.tipo_item = item_reversion.tipo_item
                item.padre = None
                item.adan = None
                item.cain = None
                item.tipo_relacion = None
                item.linea_base = item_reversion.linea_base
                item.save()
                
                # Version del item guardada.
                version_item = VersionItem.objects.create(version=item.version, id_item=item.id, nombre=item.nombre, 
                                                          descripcion=item.descripcion, costo_monetario=item.costo_monetario, 
                                                          costo_temporal=item.costo_temporal, complejidad=item.complejidad,
                                                          estado=item.estado, fase=item.fase, tipo_item=item.tipo_item,
                                                          adan=None, cain=None, padre = None, tipo_relacion=None, 
                                                          linea_base=item.linea_base, fecha_version=datetime.datetime.now())
                version_item.save()
            
                ctx = {"item_reversion":item_reversion, "item":item, "fase":fase, "proyecto":proyecto, "posee_padre":posee_padre, "existe_padre":existe_padre, "estado_padre_valido":estado_padre_valido, "estado_valido":estado_valido, "fase_valida":fase_valida, 'posee_hijos':posee_hijos}
                return render_to_response('item/confirmacion_reversionar_item.html', ctx, context_instance=RequestContext(request))
            # Fin--> Si el padre (del item a reversionar) no existe o el padre posee un estado no valido.
        # Fin--> Si el item a reversionar posee un padre/antecesor.
        # Si el item a reversionar no posee un padre/antecesor.
        else:
            item.nombre = item_reversion.nombre
            item.version = item_reversion.version
            item.estado = item_reversion.estado
            item.descripcion = item_reversion.descripcion
            item.costo_monetario = item_reversion.costo_monetario
            item.costo_temporal = item_reversion.costo_temporal
            item.complejidad = item_reversion.complejidad
            item.fase = item_reversion.fase
            item.tipo_item = item_reversion.tipo_item
            item.padre = None
            item.adan = None
            item.cain = None
            item.tipo_relacion = None
            item.linea_base = item_reversion.linea_base
            item.save()
            
            ctx = {"item_reversion":item_reversion, "item":item, "fase":fase, "proyecto":proyecto, "posee_padre":posee_padre, "estado_valido":estado_valido, "fase_valida":fase_valida, 'posee_hijos':posee_hijos}
            return render_to_response('item/confirmacion_reversionar_item.html', ctx, context_instance=RequestContext(request))
        # Fin--> Si el item a reversionar no posee un padre/antecesor.
    # Fin--> Si el estado del item a reemplazar con la reversion no es Aprobado ni Bloqueado, el estado de la fase no es Finalizado y el item a reversionar no posee hijos/sucesores.
    # Si el estado (del item a reemplazar con la reversion) es Aprobado o Bloqueado, o el estado de la fase es Finalizado, o el item a reversionar posee hijos/sucesores.
    else:
        ctx = {"item_reversion":item_reversion, "item":item, "fase":fase, "proyecto":proyecto, "estado_valido":estado_valido, "fase_valida":fase_valida, 'posee_hijos':posee_hijos}
        return render_to_response('item/confirmacion_reversionar_item.html', ctx, context_instance=RequestContext(request))
    # Fin--> Si el estado (del item a reemplazar con la reversion) es Aprobado o Bloqueado, o el estado de la fase es Finalizado, o el item a reversionar posee hijos/sucesores.

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar lineas base de fase")
@miembro_proyecto()
@rol_fase_requerido()
def lineas_base_fase_view(request, id_proyecto, id_fase):
    """
    ::
    
        La vista del listado de lineas base por fase. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
                - El usuario debe estar logueado.
                - El usuario debe poseer el permiso: Gestionar lineas base de fase.
                - Debe ser miembro del proyecto en cuestion.
        
        Esta vista permite al usuario listar y conocer las opciones de las lineas base por fase.
        Inicialmente, se verifican los permisos del usuario solicitante para restringir (si es necesario) 
        los botones de accion sobre cada linea base.
                
        La vista recibe los siguientes parametros:
    
                - request: contiene informacion sobre la sesion actual.
                - id_fase: el identificador de la fase.
            
        La vista retorna lo siguiente:
        
                - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    crear_linea_base = False
    cerrar_linea_base = False
    visualizar_linea_base = False
    gestionar_items = False
    roles = request.user.roles.all()
    for r in roles:
        for p in r.permisos.all():
            if p.nombre == 'Crear linea base':
                crear_linea_base = True
            elif p.nombre == 'Cerrar linea base':
                cerrar_linea_base= True
            elif p.nombre == 'Visualizar linea base':
                visualizar_linea_base = True
            elif p.nombre == 'Gestionar items de linea base':
                gestionar_items = True
                
            if crear_linea_base and cerrar_linea_base and visualizar_linea_base and  gestionar_items:
                break
        if crear_linea_base and cerrar_linea_base and visualizar_linea_base and  gestionar_items:
                break
                
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    valido = True
    if fase.estado == 0:
        valido = False
    lineas_base = fase.lineas_base.all()
    ctx = {'valido':valido, 'proyecto':proyecto, 'fase':fase, 'lineas_base':lineas_base, 'crear_linea_base':crear_linea_base, 'cerrar_linea_base':cerrar_linea_base, 'visualizar_linea_base':visualizar_linea_base,  'gestionar_items':gestionar_items}
    return render_to_response('fase/lineas_base_fase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear linea base")
@miembro_proyecto()
@rol_fase_requerido()
def crear_linea_base_view(request, id_proyecto, id_fase):
    """
    ::
    
        La vista para crear una linea base. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Crear linea base.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario crear y agregar una linea base a la fase previamente seleccionada, para lograr esto, 
        se verifica la validez de cada campo ingresado y luego se crea la linea base de acuerdo a los campos ingresados y 
        se almacena en la fase. 
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de lineas base por fase. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    estado_valido = True
    
    if fase.estado == 2:
        estado_valido = False
    
    form = CrearLineaBaseForm()
    if estado_valido:
        if request.method == "POST":
            form = CrearLineaBaseForm(request.POST)
            if form.is_valid():
                nombre = form.cleaned_data['nombre']
                descripcion = form.cleaned_data['descripcion']
                
                linea_base = LineaBase.objects.create(nombre=nombre, descripcion=descripcion, num_secuencia=fase.lineas_base.count()+1)
                linea_base.save()
                fase.lineas_base.add(linea_base)
                fase.save()
                return HttpResponseRedirect('/desarrollo/fases/lineas_base/fase/%s/proyecto/%s'%(id_fase, id_proyecto))
                
            else:
                ctx = {'form':form, 'fase':fase, 'proyecto':proyecto, 'estado_valido':estado_valido}
                return render_to_response('linea_base/crear_linea_base.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form, 'fase':fase, 'proyecto':proyecto, 'estado_valido':estado_valido}
    return render_to_response('linea_base/crear_linea_base.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Visualizar linea base")
@miembro_proyecto()
@rol_fase_requerido()
def visualizar_linea_base_view(request, id_proyecto, id_fase, id_linea_base):
    """
    ::
    
        La vista para visualizar una linea base. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Visualizar linea base.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
    
        Esta vista permite al usuario visualizar todos los campos guardados de una linea base de la fase previamente seleccionada.
        La vista recibe los siguientes parametros:
    
            - request: contiene informacion sobre la sesion actual.
            - id_linea_base: el identificador de la linea base.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    linea_base = fase.lineas_base.get(id=id_linea_base)
    items = linea_base.items.all()
    ctx = {'linea_base': linea_base, 'items':items, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('linea_base/visualizar_linea_base.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar items de linea base")
@miembro_proyecto()
@rol_fase_requerido()
def items_linea_base_view(request, id_proyecto, id_fase, id_linea_base):
    """
    ::
    
        La vista del listado de items por linea base. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Gestionar items de linea base.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario listar y conocer las opciones de los items de la linea base previamente seleccionada.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_linea_base: identificador de la linea base.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    fase = Fase.objects.get(id=id_fase)
    proyecto = Proyecto.objects.get(id=id_proyecto)
    items = Item.objects.filter(linea_base__id=id_linea_base)
    linea_base = fase.lineas_base.get(id=id_linea_base)
    ctx = {'fase':fase, 'proyecto':proyecto, 'items':items, 'linea_base':linea_base}
    return render_to_response('linea_base/items_linea_base.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@miembro_proyecto()
@rol_fase_requerido()
def linea_base_agregar_item_view(request, id_proyecto, id_fase, id_linea_base):
    """
    ::
    
        La vista del listado de items de la fase ligados a la linea base. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            
        Esta vista permite al usuario listar todos los items de la fase al cual esta ligada la linea base, ademas, el template relacionado concede 
        las opciones para agregar un item seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_linea_base: el identificador de la linea base.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    fase = Fase.objects.get(id=id_fase)
    proyecto = fase.proyecto
    items = fase.items.filter(estado=1)
    linea_base = fase.lineas_base.get(id=id_linea_base)
    ctx = {'fase':fase, 'proyecto':proyecto, 'items':items, 'linea_base':linea_base}
    return render_to_response('linea_base/agregar_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar item a linea base")
@miembro_proyecto()
@rol_fase_requerido()
def linea_base_confirmacion_agregar_item_view(request, id_proyecto, id_fase, id_linea_base, id_item):
    """
    ::
    
        La vista de confirmacion de agregacion de un item a una linea base. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Agregar item a linea base.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario agregar un item seleccionado a la linea base seleccionada previamente. Se verifica si el item a agregar ya 
        pertenece a la linea base, en cuyo caso se cancelara la operacion.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_item: el identificador del item.
            - id_linea_base: el identificador de la linea base.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    linea_base = fase.lineas_base.get(id=id_linea_base)
    item = fase.items.get(id=id_item)
    existe_item = True
    item_lb = False
    try:
        item = linea_base.items.get(id=id_item)
    except item.DoesNotExist:
        existe_item = False
    if item.linea_base:
        item_lb = True   
    
    if existe_item == False and item_lb == False:
        linea_base.items.add(item)
        linea_base.save()
        item.version = VersionItem.objects.filter(id_item=item.id).latest('id').version + 1
        item.save()
        
        version_item = VersionItem.objects.create(version=item.version, id_item=item.id, nombre=item.nombre, 
                                                  descripcion=item.descripcion, costo_monetario=item.costo_monetario, 
                                                  costo_temporal=item.costo_temporal, complejidad=item.complejidad,
                                                  estado=item.estado, fase=item.fase, tipo_item=item.tipo_item,
                                                  linea_base=item.linea_base, adan=item.adan, cain=item.cain, 
                                                  tipo_relacion=item.tipo_relacion, fecha_version=datetime.datetime.now())
        if item.padre:
            version_item.padre = item.padre.id
        version_item.save()
        
    ctx = {'fase':fase, 'item':item, 'linea_base':linea_base, 'proyecto':proyecto, 'existe_item':existe_item, 'item_lb':item_lb}
    return render_to_response('linea_base/confirmacion_agregar_item.html', ctx, context_instance=RequestContext(request))  

@login_required(login_url='/login/')
@permiso_requerido(permiso="Quitar item de linea base")
@miembro_proyecto()
@rol_fase_requerido()
def linea_base_quitar_item_view(request, id_proyecto, id_fase, id_item, id_linea_base):
    """
    ::
    
        La vista para quitar un item de una linea base. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Quitar item de linea base.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
        
        Esta vista permite al usuario quitar un item seleccionado de la linea base seleccionada previamente.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_item: el identificador del item.
            - id_linea_base: el identificador del linea base.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    linea_base = fase.lineas_base.get(id=id_linea_base)
    item = linea_base.items.get(id=id_item)
    linea_base.items.remove(item)
    linea_base.save()
    
    item.version = VersionItem.objects.filter(id_item=item.id).latest('id').version + 1
    item.save()
        
    version_item = VersionItem.objects.create(version=item.version, id_item=item.id, nombre=item.nombre, 
                                              descripcion=item.descripcion, costo_monetario=item.costo_monetario, 
                                              costo_temporal=item.costo_temporal, complejidad=item.complejidad,
                                              estado=item.estado, fase=item.fase, tipo_item=item.tipo_item,
                                              linea_base=None, adan=item.adan, cain=item.cain,
                                              tipo_relacion=item.tipo_relacion, fecha_version=datetime.datetime.now())
    if item.padre:
        version_item.padre = item.padre.id
    version_item.save()
    
    ctx = {'fase':fase, 'item':item, 'linea_base':linea_base,  'proyecto':proyecto}
    return render_to_response('linea_base/quitar_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Cerrar linea base")
@miembro_proyecto()
@rol_fase_requerido()
def cerrar_linea_base_view(request, id_proyecto, id_fase, id_linea_base):
    """
    ::
    
        La vista para cerrar una linea base. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Cerrar linea base.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario cerrar una linea base si es que cumple con las siguientes condiciones:
        
            - Debe estar en estado Abierta.
            - Todos sus items deben estar en estado Bloqueado.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_linea_base: el identificador de la linea base
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    fase = Fase.objects.get(id=id_fase)
    proyecto = Proyecto.objects.get(id=id_proyecto)
    linea_base = fase.lineas_base.get(id=id_linea_base)
    
    estado_valido = True
    if linea_base.estado == 1:
        estado_valido = False
    
    if estado_valido:
        items = linea_base.items.all()
        for i in items:
            existe_version = True
            i.estado = 2
            i.save()
            try:
                i.version = VersionItem.objects.filter(id_item=i.id).latest('id').version + 1
                i.save()
            except VersionItem.DoesNotExist:
                existe_version = False
            if existe_version:
                version_i = VersionItem.objects.create(version=i.version, id_item=i.id, nombre=i.nombre, 
                                                       descripcion=i.descripcion, costo_monetario=i.costo_monetario, 
                                                       costo_temporal=i.costo_temporal, complejidad=i.complejidad,
                                                       estado=i.estado, fase=i.fase, tipo_item=i.tipo_item,
                                                       linea_base=i.linea_base, adan=i.adan, cain=i.cain,
                                                       tipo_relacion=i.tipo_relacion, fecha_version=datetime.datetime.now())
                if i.padre:
                    version_i.padre = i.padre.id
                version_i.save()
            
        linea_base.estado = 1
        linea_base.save()

    ctx = {'fase':fase, 'estado_valido':estado_valido, 'proyecto':proyecto, 'linea_base':linea_base}
    return render_to_response('linea_base/cerrar_linea_base.html', ctx, context_instance=RequestContext(request))



@login_required(login_url='/login/')
@miembro_proyecto()
def reporte_proyecto_view(request, id_proyecto):
    """
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fases = Fase.objects.filter(proyecto_id=id_proyecto)
    items = []
    
    for p in fases:
        items = items + list(Item.objects.filter(fase_id=p.id))
        
    ctx = {'pagesize':'A4','proyecto':proyecto, 'fases':fases, 'items':items}
    html = render_to_string('desarrollo/reporte_proyecto.html', ctx, context_instance=RequestContext(request))
    return generar_pdf(html)

def generar_pdf(html):
    """
    Funcion para generar el archivo PDF y devolverlo mediante HttpResponse
    """
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html)) 