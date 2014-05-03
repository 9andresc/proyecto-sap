from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from administracion.models import Proyecto, Fase, TipoItem, ValorAtributo
from desarrollo.models import Item
from desarrollo.forms import CrearItemForm, ModificarItemForm
from inicio.decorators import permiso_requerido, miembro_proyecto, fase_miembro_proyecto, item_miembro_proyecto

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
    roles = request.user.roles.all()
    for r in roles:
        for p in r.permisos.all():
            if p.nombre == 'Calcular costo de proyecto':
                calcular_costo = True
            elif p.nombre == 'Gestionar fases de proyecto':
                gestionar_fases = True
                
            if calcular_costo and gestionar_fases:
                break
        if calcular_costo and gestionar_fases:
                break
            
    proyectos = Proyecto.objects.filter(estado=1)
    ctx = {'proyectos': proyectos, 'calcular_costo':calcular_costo, 'gestionar_fases':gestionar_fases}
    return render_to_response('desarrollo.html', ctx, context_instance=RequestContext(request))

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
                    costo_total = costo_total + i.costo
    ctx = {'proyecto':proyecto, 'fases_valido':fases_valido, 'items_valido':items_valido, 'costo_total':costo_total}
    return render_to_response('costo_total.html', ctx, context_instance=RequestContext(request))
            
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
            
        Esta vista permite al usuario listar y conocer las opciones de desarrollo de las fases del proyecto seleccionado.
        Inicialmente, se verifican los permisos del usuario solicitante para restringir (si es necesario) 
        los botones de accion sobre cada fase.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
    
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    iniciar_fase = False
    finalizar_fase = False
    gestionar_items = False
    roles = request.user.roles.all()
    for r in roles:
        for p in r.permisos.all():
            if p.nombre == 'Iniciar fase':
                iniciar_fase = True
            elif p.nombre == 'Finalizar fase':
                finalizar_fase = True
            elif p.nombre == 'Gestionar items de fase':
                gestionar_items = True
                
            if iniciar_fase and finalizar_fase and gestionar_items:
                break
        if iniciar_fase and finalizar_fase and gestionar_items:
                break
    
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fases = proyecto.fases.all()
    ctx = {'proyecto':proyecto, 'fases':fases, 'iniciar_fase':iniciar_fase, 'finalizar_fase':finalizar_fase, 'gestionar_items':gestionar_items}
    return render_to_response('fases_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Iniciar fase")
@fase_miembro_proyecto()
def iniciar_fase_view(request, id_fase, id_proyecto):
    """
    ::
    
        La vista para iniciar una fase. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Iniciar fase.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario iniciar una fase si es que cumple con las siguientes condiciones:
        
            - Debe estar en estado Inactivo.
            - Debe poseer al menos un item.
            - Debe poseer al menos un rol.
            
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
    items_valido = True
    roles_valido = True
    
    if fase.estado != 0:
        estado_valido = False
        inicio_valido = False
    if fase.items.count() == 0:
        items_valido = False
        inicio_valido = False
    if fase.roles.count() == 0:
        roles_valido = False
        inicio_valido = False
    
    if inicio_valido:
        fase.estado = 1
        fase.save()
        ctx = {'fase':fase, 'inicio_valido':inicio_valido, 'estado_valido':estado_valido, 'items_valido':items_valido, 'roles_valido':roles_valido, 'proyecto':proyecto}
        return render_to_response('iniciar_fase.html', ctx, context_instance=RequestContext(request))
    else:
        ctx = {'fase':fase, 'inicio_valido':inicio_valido, 'estado_valido':estado_valido, 'items_valido':items_valido, 'roles_valido':roles_valido, 'proyecto':proyecto}
        return render_to_response('iniciar_fase.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Finalizar fase")
@fase_miembro_proyecto()
def finalizar_fase_view(request, id_fase, id_proyecto):
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
    fase = Fase.objects.get(id=id_fase)
    proyecto = Proyecto.objects.get(id=id_proyecto)
    finalizado_valido = True
    estado_valido = True
    
    if fase.estado != 1:
        estado_valido = False
        finalizado_valido = False
    
    if estado_valido:
        finalizado_valido = True
        items = fase.items.all()
        for i in items:
            if i.estado != 2:
                finalizado_valido = False
                break
            
        if finalizado_valido:
            fase.estado = 2
            fase.save()
            ctx = {'fase':fase, 'finalizado_valido':finalizado_valido, 'estado_valido':estado_valido, 'proyecto':proyecto}
            return render_to_response('finalizar_fase.html', ctx, context_instance=RequestContext(request))
        else:
            ctx = {'fase':fase, 'finalizado_valido':finalizado_valido, 'estado_valido':estado_valido, 'proyecto':proyecto}
            return render_to_response('finalizar_fase.html', ctx, context_instance=RequestContext(request))
    else:
        ctx = {'fase':fase, 'finalizado_valido':finalizado_valido, 'estado_valido':estado_valido, 'proyecto':proyecto}
        return render_to_response('finalizar_fase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar items de fase")
@fase_miembro_proyecto()
def items_fase_view(request, id_fase, id_proyecto):
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
                
            if crear_item and modificar_item and eliminar_item and visualizar_item:
                break
        if crear_item and modificar_item and eliminar_item and visualizar_item:
            break
    
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = Fase.objects.get(id=id_fase)
    items = fase.items.all()
    ctx = {'proyecto':proyecto, 'fase':fase, 'items':items, 'crear_item':crear_item, 'modificar_item':modificar_item, 'eliminar_item':eliminar_item, 'visualizar_item':visualizar_item}
    return render_to_response('items_fase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear item")
@fase_miembro_proyecto()
def crear_item_view(request, id_fase, id_proyecto):
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
    fase = Fase.objects.get(id=id_fase[0])
    proyecto = Proyecto.objects.get(id=id_proyecto[0])
    form = CrearItemForm()
    if request.method == "POST":
        form = CrearItemForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            complejidad = form.cleaned_data['complejidad']
            costo = form.cleaned_data['costo']
            tipo_item = form.cleaned_data['tipo_item']
            
            tipo_item = TipoItem.objects.get(id=tipo_item)
            
            item = Item.objects.create(nombre=nombre, descripcion=descripcion, complejidad=complejidad, costo=costo, tipo_item=tipo_item)
            item.save()
            tipos_atributo = tipo_item.tipos_atributo.all()
            for tipo_atributo in tipos_atributo:
                valor_atributo = ValorAtributo.objects.create(item=item, tipo_item=tipo_item, tipo_atributo=tipo_atributo)
                valor_atributo.save()
            fase.items.add(item)
            fase.save()
            return HttpResponseRedirect('/desarrollo/items/fase/%s/proyecto/%s/'%(fase.id, proyecto.id))
            
        else:
            ctx = {'form':form, 'fase':fase, 'proyecto':proyecto}
            return render_to_response('crear_item.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('crear_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Modificar item")
@item_miembro_proyecto()
def modificar_item_view(request, id_item, id_fase, id_proyecto):
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
    item = Item.objects.get(id=id_item)
    identificador_fase = []
    for s in id_fase.split('/'):
        if s.isdigit():
            identificador_fase.append(s)
            break
    
    fase = Fase.objects.get(id=identificador_fase[0])
    proyecto = Proyecto.objects.get(id=id_proyecto[0])
    atributos = ValorAtributo.objects.filter(item__id=id_item)
    form = ModificarItemForm()
    if request.method == "POST":
        form = ModificarItemForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            complejidad = form.cleaned_data['complejidad']
            costo = form.cleaned_data['costo']
            
            for a in atributos:
                for key, value in request.POST.iteritems():
                    if a.tipo_atributo.nombre == key:
                        if a.tipo_atributo.tipo_dato == 0:
                            a.valor_numerico = value
                            a.save()
                        elif a.tipo_atributo.tipo_dato == 1:
                            a.valor_fecha = value
                            a.save()
                        elif a.tipo_atributo.tipo_dato == 2:
                            a.valor_texto = value
                            a.save()
                        else:
                            a.valor_logico = value
                            a.save()
                        
            item.nombre = nombre
            item.descripcion = descripcion
            item.complejidad = complejidad
            item.costo = costo
            item.save()
            return HttpResponseRedirect('/desarrollo/items/item/%s/fase/%s/proyecto/%s/'%(item.id, fase.id, proyecto.id))
    
    if request.method == "GET":
        form = ModificarItemForm(initial={
            'nombre': item.nombre,
            'descripcion': item.descripcion,
            'costo': item.costo,
            'complejidad': item.complejidad,
            })
    ctx = {'form':form, 'item':item, 'fase':fase, 'proyecto':proyecto, 'atributos':atributos}
    return render_to_response('modificar_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Eliminar item")
@item_miembro_proyecto()
def eliminar_item_view(request, id_item, id_fase, id_proyecto):
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
    item = Item.objects.get(id=id_item)
    identificador_fase = []
    for s in id_fase.split('/'):
        if s.isdigit():
            identificador_fase.append(s)
            break
    
    fase = Fase.objects.get(id=identificador_fase[0])
    proyecto = Proyecto.objects.get(id=id_proyecto[0])
    valido = True
    if item.estado == 1 or item.estado == 2 or item.estado == 4:
        valido = False
    if request.method == "POST":
        if valido == True:
            item.delete()
            return HttpResponseRedirect('/desarrollo/items/fase/%s/proyecto/%s/'%(fase.id, proyecto.id))
        else:
            ctx = {'item':item, 'fase':fase, 'proyecto':proyecto, 'valido':valido}
            return render_to_response('eliminar_item.html', ctx, context_instance=RequestContext(request))
    if request.method == "GET":
        ctx = {'item':item, 'fase':fase, 'proyecto':proyecto, 'valido':valido}
        return render_to_response('eliminar_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Visualizar item")
@item_miembro_proyecto()
def visualizar_item_view(request, id_item, id_fase, id_proyecto):
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
    item = Item.objects.get(id=id_item)
    atributos = ValorAtributo.objects.filter(item__id=id_item)
    fase = Fase.objects.get(id=id_fase)
    proyecto = Proyecto.objects.get(id=id_proyecto)
    ctx = {'item':item, 'fase': fase, 'proyecto':proyecto, 'atributos':atributos}
    return render_to_response('visualizar_item.html', ctx, context_instance=RequestContext(request))