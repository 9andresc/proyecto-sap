import datetime
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from administracion.models import Proyecto, Rol, TipoAtributo
from desarrollo.models import Item, Fase, TipoItem, ValorAtributo, VersionItem, LineaBase
from desarrollo.forms import CrearItemForm, ModificarItemForm, CrearFaseForm, ModificarFaseForm, CrearTipoItemForm, ModificarTipoItemForm, CrearLineaBaseForm
from inicio.decorators import permiso_requerido, miembro_proyecto, fase_miembro_proyecto

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
                    costo_total = costo_total + i.costo
    ctx = {'proyecto':proyecto, 'fases_valido':fases_valido, 'items_valido':items_valido, 'costo_total':costo_total}
    return render_to_response('desarrollo/costo_total.html', ctx, context_instance=RequestContext(request))

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
    crear_fase = False
    modificar_fase = False
    eliminar_fase = False
    visualizar_fase = False
    gestionar_tipos_item = False
    gestionar_lineas_base = False
    gestionar_items = False
    gestionar_roles = False
    iniciar_fase = False
    finalizar_fase = False
    roles = request.user.roles.all()
    for r in roles:
        for p in r.permisos.all():
            if p.nombre == 'Crear fase':
                crear_fase = True
            elif p.nombre == 'Modificar fase':
                modificar_fase = True
            elif p.nombre == 'Eliminar fase':
                eliminar_fase = True
            elif p.nombre == 'Visualizar fase':
                visualizar_fase = True
            elif p.nombre == 'Gestionar tipos de item de fase':
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
                
            if crear_fase and modificar_fase and eliminar_fase and visualizar_fase and gestionar_tipos_item and gestionar_roles and iniciar_fase and finalizar_fase and gestionar_items and gestionar_lineas_base:
                break
        if crear_fase and modificar_fase and eliminar_fase and visualizar_fase and gestionar_tipos_item and gestionar_roles and iniciar_fase and finalizar_fase and gestionar_items and gestionar_lineas_base:
                break
            
    fases = proyecto.fases.all()
    ctx = {'fases':fases, 'proyecto':proyecto, 'crear_fase':crear_fase, 'modificar_fase':modificar_fase, 'eliminar_fase':eliminar_fase, 'visualizar_fase':visualizar_fase, 'gestionar_tipos_item':gestionar_tipos_item, 'gestionar_roles':gestionar_roles, 'iniciar_fase':iniciar_fase, 'finalizar_fase':finalizar_fase, 'gestionar_items':gestionar_items, 'gestionar_lineas_base':gestionar_lineas_base}
    return render_to_response('desarrollo/gestion_fases.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear fase")
@miembro_proyecto()
def crear_fase_view(request, id_proyecto):
    """
    ::
    
        La vista para crear una fase dentro de un proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Crear fase.
            - Debe ser miembro del proyecto en cuestion.
            
        Esta vista permite al usuario crear una fase para lograr esto, se verifica la validez de cada campo ingresado y 
        luego se crea la fase de acuerdo a los campos ingresados. 
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de usuarios. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    form = CrearFaseForm()
    if request.method == "POST":
        form = CrearFaseForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            duracion = form.cleaned_data['duracion']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            
            fase = Fase.objects.create(nombre=nombre, descripcion=descripcion, duracion=duracion, fecha_inicio=fecha_inicio, num_secuencia=proyecto.fases.count()+1)
            fase.save()
            proyecto.fases.add(fase)
            proyecto.save()
            return HttpResponseRedirect('/desarrollo/fases/proyecto/%s'%id_proyecto)
            
        else:
            ctx = {'form':form, 'proyecto':proyecto}
            return render_to_response('fase/crear_fase.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form, 'proyecto':proyecto}
    return render_to_response('fase/crear_fase.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Modificar fase")
@fase_miembro_proyecto()
def modificar_fase_view(request, id_fase, id_proyecto):
    """
    ::
    
        La vista para modificar una fase. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Modificar fase.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario modificar una fase previamente seleccionada, para lograr esto, 
        se verifica la validez de cada campo modificado y luego se guarda la fase de acuerdo a los campos ingresados.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template de visualizacion de la fase modificada. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    if request.method == "POST":
        form = ModificarFaseForm(data=request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            duracion = form.cleaned_data['duracion']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            
            fase.nombre = nombre
            fase.descripcion = descripcion
            fase.duracion = duracion
            fase.fecha_inicio = fecha_inicio
            fase.save()
            return HttpResponseRedirect('/desarrollo/fases/fase/%s/proyecto/%s'%(id_fase, id_proyecto))
            
    if request.method == "GET":
        form = ModificarFaseForm(initial={
            'nombre': fase.nombre,
            'descripcion': fase.descripcion,
            'presupuesto': fase.duracion,
            })
    ctx = {'form': form, 'fase': fase, 'proyecto':proyecto}
    return render_to_response('fase/modificar_fase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Eliminar fase")
@fase_miembro_proyecto()
def eliminar_fase_view(request, id_fase, id_proyecto):
    """
    ::
    
        La vista para eliminar una fase. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Eliminar fase.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario eliminar una fase previamente seleccionada, para lograr esto, 
        se verifica si la fase cumple las siguientes condiciones:
        
            - La fase debe estar en estado Inactivo.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o no se cumplieron las condiciones para eliminar, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de fases. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    valido = True
    if fase.estado == 2 or fase.estado == 1:
        valido = False
    if request.method == "POST":
        if valido == True:
            fases = proyecto.fases.filter(id__gt=id_fase)
            for f in fases:
                f.num_secuencia = f.num_secuencia - 1
                f.save()
            fase.delete()
            return HttpResponseRedirect('/desarrollo/fases/proyecto/%s'%id_proyecto)
        else:
            ctx = {'fase':fase, 'proyecto':proyecto, 'valido':valido}
            return render_to_response('fase/eliminar_fase.html', ctx, context_instance=RequestContext(request))
    if request.method == "GET":
        ctx = {'fase':fase, 'proyecto':proyecto, 'valido':valido}
        return render_to_response('fase/eliminar_fase.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Visualizar fase")
@fase_miembro_proyecto()
def visualizar_fase_view(request, id_fase, id_proyecto):
    """
    ::
    
        La vista para visualizar una fase. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Visualizar fase.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario visualizar todos los campos guardados de una fase previamente seleccionada.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    ctx = {'fase':fase, 'proyecto':proyecto}
    return render_to_response('fase/visualizar_fase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@fase_miembro_proyecto()
def subir_fase_view(request, id_fase, id_proyecto):
    """
    ::
    
        La vista para subir de secuencia una fase. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario subir el numero de secuencia de una fase y por medio de ello bajar el numero de secuencia de la
        fase ubicada inmediatamente arriba de la fase seleccionada para subir. Sin embargo, para poder subir el numero de secuencia
        se deben cumplir los siguientes requisitos:
            
            - La fase a subir no debe estar en estado Finalizado y ninguno de sus items debe ser sucesor o antecesor de los items 
            de sus dos fases vecinas (la inmediatamente superior e inferior).
            - La fase de arriba debe cumplir los mismos requisitos que la fase a subir.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    subir_valido = True
    secuencia_valida = True
    f_estado_valido = True
    fs_estado_valido = True
    f_relaciones_valida = True
    fs_relaciones_valida = True
    if fase.num_secuencia == 1:
        secuencia_valida = False
    if fase.estado == 2:
        f_estado_valido = False
    if fase.items.count() > 0:
        items = fase.items.all()
        for i in items:
            if i.tipo_relacion == 1:
                f_relaciones_valida = False
                break
            if i.relaciones.count() > 0:
                relaciones = i.relaciones.all()
                for r in relaciones:
                    if r.tipo_relacion == 1:
                        f_relaciones_valida = False
                        break
    if fase.num_secuencia > 1:
        fase_superior = proyecto.fases.get(num_secuencia=(fase.num_secuencia - 1))
        if fase_superior.estado == 1:
            fs_estado_valido = False
        if fase_superior.items.count() > 0:
            items = fase_superior.items.all()
            for i in items:
                if i.tipo_relacion == 1:
                    fs_relaciones_valida = False
                    break
                if i.relaciones.count() > 0:
                    relaciones = i.relaciones.all()
                    for r in relaciones:
                        if r.tipo_relacion == 1:
                            fs_relaciones_valida = False
    
    if f_estado_valido and fs_estado_valido and secuencia_valida and f_relaciones_valida and fs_relaciones_valida:
        fases = proyecto.fases.all()
        fase_superior = fases.get(num_secuencia=(fase.num_secuencia - 1))
        fase = fases.get(id=id_fase)
        fase.num_secuencia = fase.num_secuencia - 1
        fase.save()
        fase_superior.num_secuencia = fase_superior.num_secuencia + 1
        fase_superior.save()
        proyecto.save()
        return HttpResponseRedirect('/desarrollo/fases/proyecto/%s'%id_proyecto)
    else:
        subir_valido = False
        return HttpResponseRedirect('/desarrollo/fases/proyecto/%s'%id_proyecto)
    
@login_required(login_url='/login/')
def bajar_fase_view(request, id_fase, id_proyecto):
    """
    ::
    
        La vista para bajar de secuencia una fase. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
            
        Esta vista permite al usuario bajar el numero de secuencia de una fase y por medio de ello subir el numero de secuencia de la
        fase ubicada inmediatamente abajo de la fase seleccionada para bajar. Sin embargo, para poder bajar el numero de secuencia
        se deben cumplir los siguientes requisitos:
            
            - La fase a bajar no debe estar en estado Finalizado y ninguno de sus items debe ser sucesor o antecesor de los items 
            de sus dos fases vecinas (la inmediatamente superior e inferior).
            - La fase de abajo debe cumplir los mismos requisitos que la fase a bajar.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - num_secuencia: el numero de secuencia de la fase.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    bajar_valido = True
    secuencia_valida = True
    f_estado_valido = True
    fi_estado_valido = True
    f_relaciones_valida = True
    fi_relaciones_valida = True
    if fase.num_secuencia == proyecto.fases.count():
        secuencia_valida = False
    if fase.estado == 2:
        f_estado_valido = False
    if fase.items.count() > 0:
        items = fase.items.all()
        for i in items:
            if i.tipo_relacion == 1:
                f_relaciones_valida = False
                break
            if i.relaciones.count() > 0:
                relaciones = i.relaciones.all()
                for r in relaciones:
                    if r.tipo_relacion == 1:
                        f_relaciones_valida = False
                        break
    if fase.num_secuencia < proyecto.fases.count():
        fase_inferior = proyecto.fases.get(num_secuencia=(fase.num_secuencia + 1))
        if fase_inferior.estado == 1:
            fi_estado_valido = False
        if fase_inferior.items.count() > 0:
            items = fase_inferior.items.all()
            for i in items:
                if i.tipo_relacion == 1:
                    fi_relaciones_valida = False
                    break
                if i.relaciones.count() > 0:
                    relaciones = i.relaciones.all()
                    for r in relaciones:
                        if r.tipo_relacion == 1:
                            fi_relaciones_valida = False
    
    if f_estado_valido and fi_estado_valido and secuencia_valida and f_relaciones_valida and fi_relaciones_valida:
        fase_inferior = proyecto.fases.get(num_secuencia=(fase.num_secuencia + 1))
        fase.num_secuencia = fase.num_secuencia + 1
        fase.save()
        fase_inferior.num_secuencia = fase_inferior.num_secuencia - 1
        fase_inferior.save()
        proyecto.save()
        return HttpResponseRedirect('/desarrollo/fases/proyecto/%s'%id_proyecto)
    else:
        bajar_valido = False
        return HttpResponseRedirect('/desarrollo/fases/proyecto/%s'%id_proyecto)
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar roles de fase")
@fase_miembro_proyecto()
def roles_fase_view(request, id_fase, id_proyecto):
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
@fase_miembro_proyecto()
def fase_agregar_rol_view(request, id_fase, id_proyecto):
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
    ctx = {'fase':fase, 'proyecto':proyecto, 'roles':roles}
    return render_to_response('fase/agregar_rol.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar rol a fase")
@fase_miembro_proyecto()
def fase_confirmacion_agregar_rol_view(request, id_fase, id_rol, id_proyecto):
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
    valido = False
    fase = Fase.objects.get(id=id_fase)
    proyecto = fase.proyecto
    rol = Rol.objects.get(id=id_rol)
    try:
        role = fase.roles.get(id=id_rol)
    except Rol.DoesNotExist:
        valido = True      
    if valido:
        fase.roles.add(rol)
        fase.save()
    ctx = {'fase':fase, 'rol':rol, 'proyecto':proyecto, 'valido':valido}
    return render_to_response('fase/confirmacion_agregar_rol.html', ctx, context_instance=RequestContext(request))  
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Quitar rol de fase")
@fase_miembro_proyecto()
def fase_quitar_rol_view(request, id_fase, id_rol, id_proyecto):
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
    fase.roles.remove(rol)
    fase.save()
    ctx = {'fase':fase, 'rol':rol, 'proyecto':proyecto}
    return render_to_response('fase/quitar_rol.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar tipos de item de fase")
@fase_miembro_proyecto()
def tipos_item_fase_view(request, id_fase, id_proyecto):
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
@fase_miembro_proyecto()
def crear_tipo_item_view(request, id_fase, id_proyecto):
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
    form = CrearTipoItemForm()
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
            ctx = {'form':form, 'fase':fase, 'proyecto':proyecto}
            return render_to_response('tipo_item/crear_tipo_item.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('tipo_item/crear_tipo_item.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Modificar tipo de item")
@fase_miembro_proyecto()
def modificar_tipo_item_view(request, id_fase, id_tipo_item, id_proyecto):
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
    ctx = {'form': form, 'tipo_item': tipo_item, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('tipo_item/modificar_tipo_item.html', ctx, context_instance=RequestContext(request))
  
@login_required(login_url='/login/')
@permiso_requerido(permiso="Visualizar tipo de item")
@fase_miembro_proyecto()
def visualizar_tipo_item_view(request, id_fase, id_tipo_item, id_proyecto):
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
@fase_miembro_proyecto()
def eliminar_tipo_item_view(request, id_fase, id_tipo_item, id_proyecto):
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
    if request.method == "POST":
        tipo_item.delete()
        return HttpResponseRedirect('/desarrollo/fases/tipos_item/fase/%s/proyecto/%s'%(id_fase, id_proyecto))
    if request.method == "GET":
        ctx = {'tipo_item':tipo_item, 'fase':fase, 'proyecto':proyecto}
        return render_to_response('tipo_item/eliminar_tipo_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar tipos de atributo de tipo de item")
@fase_miembro_proyecto()
def tipos_atributo_tipo_item_view(request, id_fase, id_tipo_item, id_proyecto):
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
@fase_miembro_proyecto()
def agregar_tipo_atributo_view(request, id_fase, id_tipo_item, id_proyecto):
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
    ctx = {'tipo_item':tipo_item, 'tipos_atributo':tipos_atributo, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('tipo_item/agregar_tipo_atributo.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar tipo de atributo a tipo de item")
@fase_miembro_proyecto()
def confirmacion_agregar_tipo_atributo_view(request, id_fase, id_tipo_atributo, id_tipo_item, id_proyecto):
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
    valido = False
    tipo_item = TipoItem.objects.get(id=id_tipo_item)
    tipo_atributo = TipoAtributo.objects.get(id=id_tipo_atributo)
    try:
        tipo_atribut = tipo_item.tipos_atributo.get(id=id_tipo_atributo)
    except TipoAtributo.DoesNotExist:
        valido = True      
    if valido:
        tipo_item.tipos_atributo.add(tipo_atributo)
        tipo_item.save()
    ctx = {'tipo_item':tipo_item, 'tipo_atributo':tipo_atributo, 'valido':valido, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('tipo_item/confirmacion_agregar_tipo_atributo.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Quitar tipo de atributo de tipo de item")
@fase_miembro_proyecto()
def quitar_tipo_atributo_view(request, id_fase, id_tipo_atributo, id_tipo_item, id_proyecto):
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
    valido = True
    if atributos:
        valido = False
    if valido:
        tipo_item.tipos_atributo.remove(tipo_atributo)
        tipo_item.save()
    ctx = {'tipo_item':tipo_item, 'tipo_atributo':tipo_atributo, 'valido':valido, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('tipo_item/quitar_tipo_atributo.html', ctx, context_instance=RequestContext(request))

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
            return render_to_response('fase/finalizar_fase.html', ctx, context_instance=RequestContext(request))
        else:
            ctx = {'fase':fase, 'finalizado_valido':finalizado_valido, 'estado_valido':estado_valido, 'proyecto':proyecto}
            return render_to_response('fase/finalizar_fase.html', ctx, context_instance=RequestContext(request))
    else:
        ctx = {'fase':fase, 'finalizado_valido':finalizado_valido, 'estado_valido':estado_valido, 'proyecto':proyecto}
        return render_to_response('fase/finalizar_fase.html', ctx, context_instance=RequestContext(request))

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
    gestionar_relaciones = False
    aprobar_item = False
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
                
            if crear_item and modificar_item and eliminar_item and visualizar_item and gestionar_relaciones and aprobar_item:
                break
        if crear_item and modificar_item and eliminar_item and visualizar_item and gestionar_relaciones and aprobar_item:
            break
    
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    valido = True
    if fase.estado == 0:
        valido = False
    items = fase.items.all()
    ctx = {'valido':valido, 'proyecto':proyecto, 'fase':fase, 'items':items, 'crear_item':crear_item, 'modificar_item':modificar_item, 'eliminar_item':eliminar_item, 'visualizar_item':visualizar_item, 'gestionar_relaciones':gestionar_relaciones, 'aprobar_item':aprobar_item}
    return render_to_response('fase/items_fase.html', ctx, context_instance=RequestContext(request))

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
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    tipos_item = fase.tipos_item.all()
    
    form = CrearItemForm()
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
            item.save()
            version_item = VersionItem.objects.create(id_item=item.id, nombre=nombre, descripcion=descripcion, complejidad=complejidad, costo_monetario=costo_monetario, costo_temporal=costo_temporal, fase=fase, tipo_item=tipo_item, fecha_version=datetime.datetime.now())
            version_item.save()
            tipos_atributo = tipo_item.tipos_atributo.all()
            for tipo_atributo in tipos_atributo:
                valor_atributo = ValorAtributo.objects.create(item=item, tipo_item=tipo_item, tipo_atributo=tipo_atributo)
                valor_atributo.save()
            fase.items.add(item)
            fase.save()
            return HttpResponseRedirect('/desarrollo/fases/items/fase/%s/proyecto/%s'%(id_fase, id_proyecto))
            
        else:
            ctx = {'form':form, 'fase':fase, 'proyecto':proyecto, 'tipos_item':tipos_item}
            return render_to_response('crear_item.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form, 'fase':fase, 'proyecto':proyecto, 'tipos_item':tipos_item}
    return render_to_response('item/crear_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Modificar item")
@fase_miembro_proyecto()
def modificar_item_view(request, id_fase, id_item, id_proyecto):
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
    fase = Fase.objects.get(id=id_fase)
    proyecto = Proyecto.objects.get(id=id_proyecto)
    atributos = ValorAtributo.objects.filter(item__id=id_item)
    form = ModificarItemForm()
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
                            a.valor_numerico = value
                            a.save()
                        elif a.tipo_atributo.tipo_dato == 1:
                            a.valor_fecha = value
                            a.save()
                        elif a.tipo_atributo.tipo_dato == 2:
                            a.valor_texto = value
                            a.save()
                        else:
                            if value=="1":
                                a.valor_logico = None
                                a.save()
                            elif value=="2":
                                a.valor_logico = True
                                a.save()
                            elif value=="3":
                                a.valor_logico = False
                                a.save()
                        
            item.nombre = nombre
            item.descripcion = descripcion
            item.complejidad = complejidad
            item.costo_monetario = costo_monetario
            item.costo_temporal = costo_temporal
            item.save()
            version = VersionItem.objects.filter(id_item=item.id).order_by('-fecha_version')[:1]
            version_item = VersionItem.objects.create(version = version[0].version + 0.1, id_item=item.id, nombre=nombre, descripcion=descripcion, complejidad=complejidad, costo_monetario=costo_monetario, costo_temporal=costo_temporal, fase=item.fase, tipo_item=item.tipo_item, fecha_version=datetime.datetime.now())
            version_item.save()
            return HttpResponseRedirect('/desarrollo/fases/items/item/%s/fase/%s/proyecto/%s'%(id_item, id_fase, id_proyecto))
    
    if request.method == "GET":
        form = ModificarItemForm(initial={
            'nombre': item.nombre,
            'descripcion': item.descripcion,
            'costo_temporal': item.costo_temporal,
            'costo_monetario': item.costo_monetario,
            'complejidad': item.complejidad,
            })
    ctx = {'form':form, 'item':item, 'fase':fase, 'proyecto':proyecto, 'atributos':atributos}
    return render_to_response('item/modificar_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Eliminar item")
@fase_miembro_proyecto()
def eliminar_item_view(request, id_fase, id_item, id_proyecto):
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
    atributos = ValorAtributo.objects.filter(item__id=id_item)
    fase = Fase.objects.get(id=id_fase)
    proyecto = Proyecto.objects.get(id=id_proyecto)
    valido = True
    if item.estado == 1 or item.estado == 2 or item.estado == 4:
        valido = False
    if request.method == "POST":
        if valido == True:
            item.delete()
            return HttpResponseRedirect('/desarrollo/fases/items/fase/%s/proyecto/%s'%(id_fase, id_proyecto))
        else:
            ctx = {'item':item, 'fase':fase, 'proyecto':proyecto, 'valido':valido, 'atributos':atributos}
            return render_to_response('item/eliminar_item.html', ctx, context_instance=RequestContext(request))
    if request.method == "GET":
        ctx = {'item':item, 'fase':fase, 'proyecto':proyecto, 'valido':valido, 'atributos':atributos}
        return render_to_response('item/eliminar_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Visualizar item")
@fase_miembro_proyecto()
def visualizar_item_view(request, id_fase, id_item, id_proyecto):
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
    return render_to_response('item/visualizar_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Aprobar item")
@fase_miembro_proyecto()
def aprobar_item_view(request, id_fase, id_item, id_proyecto):
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
    valido = True
    if item.estado == 1 or item.estado == 2:
        valido = False
    if valido:
        item.estado = 1
        item.save()
    ctx = {'item':item, 'valido':valido, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('item/aprobar_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar relaciones de item")
@fase_miembro_proyecto()
def relaciones_item_view(request, id_fase, id_item, id_proyecto):
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
    relaciones = item.relaciones.all()
    ctx = {'item':item, 'relaciones':relaciones, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('item/relaciones_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@fase_miembro_proyecto()
def agregar_relacion_view(request, id_fase, id_item, id_proyecto):
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
    valido = False
    if item.estado == 1 or item.estado == 2:
        valido = True
    if request.method == "POST":
        eleccion_relacion = request.POST.get('eleccion_relacion')
        if eleccion_relacion == "0":
            items_hijos = fase.items.filter(padre=None).exclude(id=id_item)
            if item.adan:
                items_hijos = items_hijos.exclude(id=item.adan)
            if item.cain:
                items_hijos = items_hijos.exclude(id=item.cain)
            ctx = {'item':item, 'items_hijos':items_hijos, 'fase':fase, 'proyecto':proyecto, 'valido':valido}
            return render_to_response('item/agregar_relacion.html', ctx, context_instance=RequestContext(request))
        elif eleccion_relacion == "1":
            estado_valido = False
            num_fases_valido = False
            if item.estado == 2:
                estado_valido = True
            num_fases = proyecto.fases.count()
            if fase.num_secuencia < num_fases:
                num_fases_valido = True
            if estado_valido and num_fases_valido:
                fase_vecina = proyecto.fases.get(num_secuencia = (fase.num_secuencia + 1))
                items_sucesores = fase_vecina.items.filter(padre=None)
                ctx = {'item':item, 'items_sucesores':items_sucesores, 'fase':fase, 'fase_vecina':fase_vecina, 'proyecto':proyecto, 'valido':valido}
                return render_to_response('item/agregar_relacion.html', ctx, context_instance=RequestContext(request))
            else:
                ctx = {'item':item, 'fase':fase, 'proyecto':proyecto, 'valido':valido, 'estado_valido':estado_valido, 'num_fases_valido':num_fases_valido}
                return render_to_response('item/agregar_relacion.html', ctx, context_instance=RequestContext(request))

    items_hijos = fase.items.filter(padre=None).exclude(id=id_item)
    if item.adan:
        items_hijos = items_hijos.exclude(id=item.adan)
    if item.cain:
        items_hijos = items_hijos.exclude(id=item.cain)
    ctx = {'item':item, 'items_hijos':items_hijos, 'fase':fase, 'proyecto':proyecto, 'valido':valido}
    return render_to_response('item/agregar_relacion.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar relacion a item")
@fase_miembro_proyecto()
def confirmacion_agregar_relacion_view(request, id_fase, id_item, id_relacion, id_proyecto):
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
    item = fase.items.get(id=id_item)
    relacion = Item.objects.get(id=id_relacion)
    if item.fase.id == relacion.fase.id:
        if item.adan:
            relacion.adan = item.adan
        else:
            relacion.adan = item.id
            
        if item.adan and item.cain == None:
            relacion.adan = item.adan
            relacion.cain = item.id
        elif item.adan and item.cain:
            relacion.cain = item.cain
            
        relacion.tipo_relacion = 0
        relacion.save()
    else:
        if item.adan:
            relacion.adan = item.adan
        else:
            relacion.adan = item.id
            
        if item.adan and item.cain == None:
            relacion.adan = item.adan
            relacion.cain = item.id
        elif item.adan and item.cain:
            relacion.cain = item.cain
        
        relacion.tipo_relacion = 1
        relacion.save()
        
    item.relaciones.add(relacion)
    item.save()

    ctx = {'item':item, 'relacion':relacion, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('item/confirmacion_agregar_relacion.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Quitar relacion de item")
@fase_miembro_proyecto()
def quitar_relacion_view(request, id_fase, id_item, id_relacion, id_proyecto):
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
    item = fase.items.get(id=id_item)
    relacion = Item.objects.get(id=id_relacion)
    
    relacion.padre_raiz = None
    relacion.padre = None
    relacion.tipo_relacion = None
    relacion.save()
    
    relaciones = relacion.relaciones.all()
    for r in relaciones:
        r.adan = relacion.id
        r.cain = None
        r.save()
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
            h.save()
            
    ctx = {'item':item, 'relacion':relacion, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('item/quitar_relacion.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar lineas base de fase")
@fase_miembro_proyecto()
def lineas_base_fase_view(request, id_fase, id_proyecto):
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
    modificar_linea_base = False
    eliminar_linea_base = False
    visualizar_linea_base = False
    gestionar_items = False
#    iniciar_fase = False
#    finalizar_fase = False
    roles = request.user.roles.all()
    for r in roles:
        for p in r.permisos.all():
            if p.nombre == 'Crear linea base':
                crear_linea_base = True
            elif p.nombre == 'Modificar linea base':
                modificar_linea_base= True
            elif p.nombre == 'Eliminar linea base':
                eliminar_linea_base = True
            elif p.nombre == 'Visualizar linea base':
                visualizar_linea_base = True
#            elif p.nombre == 'Iniciar fase':
#                iniciar_fase = True
#            elif p.nombre == 'Finalizar fase':
#                finalizar_fase = True
            elif p.nombre == 'Gestionar items de linea base':
                gestionar_items = True
                
            if crear_linea_base and modificar_linea_base and eliminar_linea_base and visualizar_linea_base and  gestionar_items:
                break
        if crear_linea_base and modificar_linea_base and eliminar_linea_base and visualizar_linea_base and  gestionar_items:
                break
                
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = proyecto.fases.get(id=id_fase)
    valido = True
    if fase.estado == 0:
        valido = False
    lineas_base = fase.lineas_base.all()
    ctx = {'valido':valido, 'proyecto':proyecto, 'fase':fase, 'lineas_base':lineas_base, 'crear_linea_base':crear_linea_base, 'modificar_linea_base':modificar_linea_base, 'eliminar_linea_base':eliminar_linea_base, 'visualizar_linea_base':visualizar_linea_base,  'gestionar_items':gestionar_items}
    return render_to_response('fase/lineas_base_fase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear linea base")
@fase_miembro_proyecto()
def crear_linea_base_view(request, id_fase, id_proyecto):
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
    
    form = CrearLineaBaseForm()
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
            ctx = {'form':form, 'fase':fase, 'proyecto':proyecto}
            return render_to_response('linea_base/crear_linea_base.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('linea_base/crear_linea_base.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Visualizar linea base")
@fase_miembro_proyecto()
def visualizar_linea_base_view(request, id_fase, id_linea_base, id_proyecto):
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
    ctx = {'linea_base': linea_base, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('linea_base/visualizar_linea_base.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar items de linea base")
@fase_miembro_proyecto()
def items_linea_base_view(request, id_fase, id_linea_base, id_proyecto):
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
    item = Item.objects.filter(fase__id=id_fase)
    linea_base = fase.lineas_base.get(id=id_linea_base)
    ctx = {'fase':fase, 'proyecto':proyecto, 'item':item, 'linea_base':linea_base}
    return render_to_response('linea_base/items_linea_base.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@fase_miembro_proyecto()
def linea_base_agregar_item_view(request, id_fase, id_linea_base, id_proyecto):
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
    items = fase.items.all()
    linea_base = fase.lineas_base.get(id=id_linea_base)
    ctx = {'fase':fase, 'proyecto':proyecto, 'items':items, 'linea_base':linea_base}
    return render_to_response('linea_base/agregar_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar item a linea base")
@fase_miembro_proyecto()
def linea_base_confirmacion_agregar_item_view(request, id_fase, id_linea_base,id_item, id_proyecto):
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
    valido = False
    fase = Fase.objects.get(id=id_fase)
    proyecto = fase.proyecto
    linea_base = LineaBase.objects.get(id=id_linea_base)
    item = Item.objects.get(id=id_item)
    try:
        item = linea_base.items.get(id=id_item)
    except item.DoesNotExist:
        valido = True      
    if valido:
        linea_base.items.add(item)
        linea_base.save()
    ctx = {'fase':fase, 'item':item, 'linea_base':linea_base, 'proyecto':proyecto, 'valido':valido}
    return render_to_response('linea_base/confirmacion_agregar_item.html', ctx, context_instance=RequestContext(request))  


@login_required(login_url='/login/')
@permiso_requerido(permiso="Cerrar linea base")
@fase_miembro_proyecto()
def cerrar_linea_base_view(request, id_fase, id_linea_base, id_proyecto):
    """
    ::
    
        La vista para visualizar una linea base. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Visualizar linea base.
            - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
    
 Esta vista permite al usuario cerrar una linea base si se cumple con los siguientes requisitos:
        
            - Debe estar en estado Abierta.
            - Debe poseer solo items en estado bloqueado.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_fase: el identificador de la fase.
            - id_linea_base: el identificador de la linea base.
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