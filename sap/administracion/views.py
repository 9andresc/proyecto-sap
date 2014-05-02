from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from administracion.forms import CrearUsuarioForm, ModificarUsuarioForm, CambiarContrasenhaForm, CrearRolForm, ModificarRolForm, CrearTipoAtributoForm, ModificarTipoAtributoForm, CrearProyectoForm, ModificarProyectoForm, CrearFaseForm, ModificarFaseForm, CrearTipoItemForm, ModificarTipoItemForm
from administracion.models import Rol, Permiso, TipoAtributo, Proyecto, Fase, TipoItem, ValorAtributo
from inicio.decorators import permiso_requerido, miembro_proyecto, fase_miembro_proyecto

@login_required(login_url='/login/')
def gestion_usuarios_view(request):
    """
    Permite listar todos los usuarios registrados en el sistema, junto con las 
    operaciones disponibles por cada usuario.
    """
    usuarios = User.objects.all()
    ctx = {'usuarios': usuarios}
    return render_to_response('usuario/gestion_usuarios.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear usuario")
def crear_usuario_view(request):
    """
    Permite crear un nuevo usuario en el sistema.
    """
    form = CrearUsuarioForm()
    if request.method == "POST":
        form = CrearUsuarioForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password_uno = form.cleaned_data['password_uno']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']
            usuario = User.objects.create_user(username=username, email=email, password=password_uno, first_name=first_name, last_name=last_name, direccion=direccion, telefono=telefono)
            usuario.save()
            return HttpResponseRedirect('/administracion/gestion_usuarios/')
        else:
            ctx = {'form':form}
            return render_to_response('usuario/crear_usuario.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('usuario/crear_usuario.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Modificar usuario")
def modificar_usuario_view(request, id_usuario):
    """
    Permite modificar un usuario existente en el sistema.
    """
    usuario = User.objects.get(id=id_usuario)
    if request.method == "POST":
        form = ModificarUsuarioForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']
            usuario.username = username
            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.direccion = direccion
            usuario.telefono = telefono
            usuario.save()
            return HttpResponseRedirect('/administracion/gestion_usuarios/usuario/%s'%usuario.id)
            
    if request.method == "GET":
        form = ModificarUsuarioForm(initial={
            'username': usuario.username,
            'email': usuario.email,
            'first_name': usuario.first_name,
            'last_name': usuario.last_name,
            'direccion': usuario.direccion,
            'telefono': usuario.telefono,
            })
    ctx = {'form': form, 'usuario': usuario}
    return render_to_response('usuario/modificar_usuario.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Cambiar contrasenha")
def cambiar_contrasenha_view(request, id_usuario):
    valido = True
    usuario = User.objects.get(id=id_usuario)
    if request.method == "POST":
        form = CambiarContrasenhaForm(request.POST)
        if form.is_valid():
            password_uno = form.cleaned_data['password_uno']
            usuario.set_password(password_uno)
            usuario.save()
            logout(request)
            return redirect('vista_login')
        else:
            valido = False
    if request.method == "GET":
        form = CambiarContrasenhaForm(initial={
            'password_uno': '',
            'password_dos': '',
            })
    ctx = {'form': form, 'valido':valido, 'usuario':usuario}
    return render_to_response('usuario/cambiar_contrasenha.html', ctx, context_instance=RequestContext(request))
            
@login_required(login_url='/login/')
@permiso_requerido(permiso="Eliminar usuario")
def eliminar_usuario_view(request, id_usuario):
    """
    Permite eliminar un usuario existente en el sistema.
    """
    usuario = User.objects.get(id=id_usuario)
    if request.method == "POST":
        User.objects.get(id=id_usuario).delete()
        return HttpResponseRedirect('/administracion/gestion_usuarios/')
    if request.method == "GET":
        ctx = {'usuario':usuario}
        return render_to_response('usuario/eliminar_usuario.html', ctx, context_instance=RequestContext(request))
        

@login_required(login_url='/login/')
@permiso_requerido(permiso="Visualizar usuario")
def visualizar_usuario_view(request, id_usuario):
    """
    Permite visualizar todos los campos de un usuario existente en el sistema.
    """
    usuario = User.objects.get(id=id_usuario)
    ctx = {'usuario': usuario}
    return render_to_response('usuario/visualizar_usuario.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar roles de usuario")
def roles_usuario_view(request, id_usuario):
    """
    Permite listar todos los roles pertenecientes a un usuario existente en el sistema, 
    junto con las operaciones de agregacion de roles y eliminacion de roles.
    """
    usuario = User.objects.get(id=id_usuario)
    roles = Rol.objects.filter(user__id=id_usuario)
    ctx = {'usuario':usuario, 'roles':roles}
    return render_to_response('usuario/roles_usuario.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def agregar_rol_view(request, id_usuario):
    """
    Permite listar todos los roles registrados en el sistema, junto con las 
    operaciones de agregacion de rol.
    """
    usuario = User.objects.get(id=id_usuario)
    roles = Rol.objects.all()
    ctx = {'usuario':usuario, 'roles':roles}
    return render_to_response('usuario/agregar_rol.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar rol a usuario")
def confirmacion_agregar_rol_view(request, id_usuario, id_rol):
    """
    Permite agregar un rol previamente seleccionado a un usuario existente en el 
    sistema.
    """
    valido = False
    usuario = User.objects.get(id=id_usuario)
    rol = Rol.objects.get(id=id_rol)
    try:
        role = usuario.roles.get(id=id_rol)
    except Rol.DoesNotExist:
        valido = True
    if valido:
        usuario.roles.add(rol)
        usuario.save()
    ctx = {'usuario':usuario, 'rol':rol, 'valido':valido}
    return render_to_response('usuario/confirmacion_agregar_rol.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Quitar rol de usuario")
def quitar_rol_view(request, id_usuario, id_rol):
    """
    Permite quitar un rol previamente seleccionado de un usuario existente en el 
    sistema.
    """
    usuario = User.objects.get(id=id_usuario)
    rol = Rol.objects.get(id=id_rol)
    usuario.roles.remove(rol)
    usuario.save()
    ctx = {'usuario':usuario, 'rol':rol}
    return render_to_response('usuario/quitar_rol.html', ctx, context_instance=RequestContext(request))
       
@login_required(login_url='/login/')
def gestion_roles_view(request):
    """
    Permite listar todos los roles registrados en el sistema, junto con las 
    operaciones disponibles por cada rol.
    """
    roles = Rol.objects.all()
    ctx = {'roles': roles}
    return render_to_response('rol/gestion_roles.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear rol")
def crear_rol_view(request):
    """
    Permite crear un nuevo rol en el sistema.
    """
    form = CrearRolForm()
    if request.method == "POST":
        form = CrearRolForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            rol = Rol.objects.create(nombre=nombre, descripcion=descripcion)
            rol.save()
            return HttpResponseRedirect('/administracion/gestion_roles/')
        else:
            ctx = {'form':form}
            return render_to_response('rol/crear_rol.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('rol/crear_rol.html', ctx, context_instance=RequestContext(request)) 

@login_required(login_url='/login/')
@permiso_requerido(permiso="Modificar rol")
def modificar_rol_view(request, id_rol):
    """
    Permite modificar un rol existente en el sistema.
    """
    rol = Rol.objects.get(id=id_rol)
    if request.method == "POST":
        form = ModificarRolForm(data=request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            rol.nombre = nombre
            rol.descripcion = descripcion
            rol.save()
            return HttpResponseRedirect('/administracion/gestion_roles/rol/%s'%rol.id)
            
    if request.method == "GET":
        form = ModificarRolForm(initial={
            'nombre': rol.nombre,
            'descripcion': rol.descripcion,
            })
    ctx = {'form': form, 'rol': rol}
    return render_to_response('rol/modificar_rol.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Eliminar rol")
def eliminar_rol_view(request, id_rol):
    """
    Permite eliminar un rol existente en el sistema.
    """
    rol = Rol.objects.get(id=id_rol)
    if request.method == "POST":
        Rol.objects.get(id=id_rol).delete()
        return HttpResponseRedirect('/administracion/gestion_roles/')
    if request.method == "GET":
        ctx = {'rol':rol}
        return render_to_response('rol/eliminar_rol.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Visualizar rol")
def visualizar_rol_view(request, id_rol):
    """
    Permite visualizar todos los campos de un rol existente en el sistema.
    """
    rol = Rol.objects.get(id=id_rol)
    ctx = {'rol': rol}
    return render_to_response('rol/visualizar_rol.html', ctx, context_instance=RequestContext(request)) 
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar permisos de rol")
def permisos_rol_view(request, id_rol):
    """
    Permite listar todos los permisos pertenecientes a un rol existente en el sistema, 
    junto con las operaciones de agregacion de permisos y eliminacion de permisos.
    """
    rol = Rol.objects.get(id=id_rol)
    permisos = Permiso.objects.filter(rol__id=id_rol)
    ctx = {'rol':rol, 'permisos':permisos}
    return render_to_response('rol/permisos_rol.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def agregar_permiso_view(request, id_rol):
    """
    Permite listar todos los permisos registrados en el sistema, junto con las 
    operaciones de agregacion de permiso.
    """
    rol = Rol.objects.get(id=id_rol)
    permisos = Permiso.objects.all()
    ctx = {'rol':rol, 'permisos':permisos}
    return render_to_response('rol/agregar_permiso.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar permiso a rol")
def confirmacion_agregar_permiso_view(request, id_rol, id_permiso):
    """
    Permite agregar un permiso previamente seleccionado a un rol existente en el 
    sistema.
    """
    valido = False
    rol = Rol.objects.get(id=id_rol)
    permiso = Permiso.objects.get(id=id_permiso)
    try:
        permis = rol.permisos.get(id=id_permiso)
    except Permiso.DoesNotExist:
        valido = True      
    if valido:
        rol.permisos.add(permiso)
        rol.save()
    ctx = {'rol':rol, 'permiso':permiso, 'valido':valido}
    return render_to_response('rol/confirmacion_agregar_permiso.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Quitar permiso de rol")
def quitar_permiso_view(request, id_rol, id_permiso):
    """
    Permite quitar un permiso previamente seleccionado de un rol existente en el 
    sistema.
    """
    rol = Rol.objects.get(id=id_rol)
    permiso = Permiso.objects.get(id=id_permiso)
    rol.permisos.remove(permiso)
    rol.save()
    ctx = {'rol':rol, 'permiso':permiso}
    return render_to_response('rol/quitar_permiso.html', ctx, context_instance=RequestContext(request))
   
       
@login_required(login_url='/login/')
def gestion_tipos_atributo_view(request):
    """
    Permite listar todos los tipos atributo registrados en el sistema, junto con las 
    operaciones disponibles por cada tipo atributo.
    """
    tipos_atributo = TipoAtributo.objects.all()
    ctx = {'tipos_atributo': tipos_atributo}
    return render_to_response('tipo_atributo/gestion_tipos_atributo.html', ctx, context_instance=RequestContext(request)) 
  
  
@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear tipo de atributo")
def crear_tipo_atributo_view(request):
    """
    Permite crear un nuevo tipo atributo en el sistema.
    """
    form = CrearTipoAtributoForm()
    if request.method == "POST":
        form = CrearTipoAtributoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            tipo_dato = form.cleaned_data['tipo_dato']
            tipo_atributo = TipoAtributo.objects.create(nombre=nombre, descripcion=descripcion, tipo_dato=tipo_dato)
            tipo_atributo.save()
            return HttpResponseRedirect('/administracion/gestion_tipos_atributo/')
            
        else:
            ctx = {'form':form}
            return render_to_response('tipo_atributo/crear_tipo_atributo.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('tipo_atributo/crear_tipo_atributo.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Modificar tipo de atributo")
def modificar_tipo_atributo_view(request, id_tipo_atributo):
    """
    Permite modificar un tipo atributo existente en el sistema.
    """
    tipo_atributo = TipoAtributo.objects.get(id=id_tipo_atributo)
    atributos = ValorAtributo.objects.filter(tipo_atributo__id=id_tipo_atributo)
    valido = True
    if atributos:
        valido = False
    if request.method == "POST":
        form = ModificarTipoAtributoForm(data=request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            tipo_dato = form.cleaned_data['tipo_dato']
            tipo_atributo.nombre = nombre
            tipo_atributo.descripcion = descripcion
            tipo_atributo.tipo_dato = tipo_dato
            tipo_atributo.save()
            return HttpResponseRedirect('/administracion/gestion_tipos_atributo/tipo_atributo/%s'%tipo_atributo.id)
            
    if request.method == "GET":
        form = ModificarTipoAtributoForm(initial={
            'nombre': tipo_atributo.nombre,
            'descripcion': tipo_atributo.descripcion,
            'tipo_dato': tipo_atributo.tipo_dato,
            })
    ctx = {'form': form, 'tipo_atributo': tipo_atributo, 'valido':valido}
    return render_to_response('tipo_atributo/modificar_tipo_atributo.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Eliminar tipo de atributo")
def eliminar_tipo_atributo_view(request, id_tipo_atributo):
    """
    Permite eliminar un tipo atributo existente en el sistema.
    """
    tipo_atributo = TipoAtributo.objects.get(id=id_tipo_atributo)
    atributos = ValorAtributo.objects.filter(tipo_atributo__id=id_tipo_atributo)
    valido = True
    if atributos:
        valido = False
    if request.method == "POST":
        TipoAtributo.objects.get(id=id_tipo_atributo).delete()
        return HttpResponseRedirect('/administracion/gestion_tipos_atributo/')
    if request.method == "GET":
        ctx = {'tipo_atributo':tipo_atributo, 'valido':valido}
        return render_to_response('tipo_atributo/eliminar_tipo_atributo.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Visualizar tipo de atributo")
def visualizar_tipo_atributo_view(request, id_tipo_atributo):
    """
    Permite visualizar todos los campos de un tipo atributo existente en el sistema.
    """
    tipo_atributo = TipoAtributo.objects.get(id=id_tipo_atributo)
    ctx = {'tipo_atributo': tipo_atributo}
    return render_to_response('tipo_atributo/visualizar_tipo_atributo.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def gestion_proyectos_view(request):
    """
    Permite listar todos los proyectos registrados en el sistema, junto con las 
    operaciones disponibles por cada proyecto.
    """
    proyectos = Proyecto.objects.all()
    ctx = {'proyectos': proyectos}
    return render_to_response('proyecto/gestion_proyectos.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear proyecto")
def crear_proyecto_view(request):
    """
    Permite crear un nuevo proyecto en el sistema.
    """
    form = CrearProyectoForm()
    if request.method == "POST":
        form = CrearProyectoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            presupuesto = form.cleaned_data['presupuesto']
            complejidad = form.cleaned_data['complejidad']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            usuario_lider = form.cleaned_data['usuario_lider']
            
            lider = User.objects.get(id=usuario_lider)
            rol_lider = Rol.objects.get(nombre="Lider de proyecto")
            lider.roles.add(rol_lider)
            
            proyecto = Proyecto.objects.create(nombre=nombre, descripcion=descripcion, presupuesto=presupuesto, complejidad=complejidad, fecha_inicio=fecha_inicio, usuario_lider=lider)
            proyecto.roles.add(rol_lider)
            proyecto.usuarios.add(lider)
            proyecto.save()
            return HttpResponseRedirect('/administracion/gestion_proyectos/')
            
        else:
            ctx = {'form':form}
            return render_to_response('proyecto/crear_proyecto.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('proyecto/crear_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Modificar proyecto")
@miembro_proyecto()
def modificar_proyecto_view(request, id_proyecto):
    """
    Permite modificar un proyecto existente en el sistema.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if request.method == "POST":
        form = ModificarProyectoForm(data=request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            presupuesto = form.cleaned_data['presupuesto']
            complejidad = form.cleaned_data['complejidad']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            usuario_lider = form.cleaned_data['usuario_lider']
            
            lider = User.objects.get(id=usuario_lider)
            
            proyecto.nombre = nombre
            proyecto.descripcion = descripcion
            proyecto.presupuesto = presupuesto
            proyecto.complejidad = complejidad
            proyecto.fecha_inicio = fecha_inicio
            proyecto.usuario_lider = lider
            proyecto.save()
            return HttpResponseRedirect('/administracion/gestion_proyectos/proyecto/%s'%proyecto.id)
            
    if request.method == "GET":
        form = ModificarProyectoForm(initial={
            'nombre': proyecto.nombre,
            'descripcion': proyecto.descripcion,
            'presupuesto': proyecto.presupuesto,
            'complejidad': proyecto.complejidad,
            })
    ctx = {'form': form, 'proyecto': proyecto}
    return render_to_response('proyecto/modificar_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Eliminar proyecto")
@miembro_proyecto()
def eliminar_proyecto_view(request, id_proyecto):
    """
    Permite eliminar un proyecto existente en el sistema.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    valido = True
    if proyecto.estado == 2 or proyecto.estado == 1:
        valido = False
    if request.method == "POST":
        if valido == True:
            proyecto = Proyecto.objects.get(id=id_proyecto)
            rol_lider = Rol.objects.get(nombre="Lider de proyecto")
            proyecto.usuario_lider.roles.remove(rol_lider)
            proyecto.delete()
            return HttpResponseRedirect('/administracion/gestion_proyectos/')
        else:
            ctx = {'proyecto':proyecto, 'valido':valido}
            return render_to_response('proyecto/eliminar_proyecto.html', ctx, context_instance=RequestContext(request))
    if request.method == "GET":
        ctx = {'proyecto':proyecto, 'valido':valido}
        return render_to_response('proyecto/eliminar_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Visualizar proyecto")
@miembro_proyecto()
def visualizar_proyecto_view(request, id_proyecto):
    """
    Permite visualizar todos los campos de un proyecto existente en el sistema.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    ctx = {'proyecto': proyecto}
    return render_to_response('proyecto/visualizar_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar usuarios de proyecto")
@miembro_proyecto()
def usuarios_proyecto_view(request, id_proyecto):
    """
    Permite listar todos los usuarios pertenecientes a un proyecto existente en el sistema, 
    junto con las operaciones de agregacion de usuarios y eliminacion de usuarios.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    usuarios = User.objects.filter(usuarios_proyecto__id=id_proyecto)
    ctx = {'proyecto':proyecto, 'usuarios':usuarios}
    return render_to_response('proyecto/usuarios_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def proyecto_agregar_usuario_view(request, id_proyecto):
    """
    Permite listar todos los usuarios registrados en el sistema, junto con las 
    operaciones de agregacion de usuario.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    usuarios = User.objects.all()
    ctx = {'proyecto':proyecto, 'usuarios':usuarios}
    return render_to_response('proyecto/agregar_usuario.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar usuario a proyecto")
@miembro_proyecto()
def confirmacion_proyecto_agregar_usuario_view(request, id_proyecto, id_usuario):
    """
    Permite agregar un usuario previamente seleccionado a un proyecto existente en el 
    sistema.
    """
    valido = False
    proyecto = Proyecto.objects.get(id=id_proyecto)
    usuario = User.objects.get(id=id_usuario)
    try:
        user = proyecto.usuarios.get(id=id_usuario)
    except User.DoesNotExist:
        valido = True      
    if valido:
        proyecto.usuarios.add(usuario)
        proyecto.save()
    ctx = {'proyecto':proyecto, 'usuario':usuario, 'valido':valido}
    return render_to_response('proyecto/confirmacion_agregar_usuario.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Quitar usuario de proyecto")
@miembro_proyecto()
def proyecto_quitar_usuario_view(request, id_proyecto, id_usuario):
    """
    Permite quitar un usuario previamente seleccionado de un proyecto existente en el 
    sistema.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    usuario = User.objects.get(id=id_usuario)
    proyecto.usuarios.remove(usuario)
    proyecto.save()
    ctx = {'proyecto':proyecto, 'usuario':usuario}
    return render_to_response('proyecto/quitar_usuario.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar fases de proyecto")
@miembro_proyecto()
def fases_proyecto_view(request, id_proyecto):
    """
    Permite listar todas las fases pertenecientes a un proyecto existente en el sistema, 
    junto con las operaciones de agregacion de fases y eliminacion de fases.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fases = proyecto.fases.all()
    ctx = {'proyecto':proyecto, 'fases':fases}
    return render_to_response('proyecto/fases_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def proyecto_agregar_fase_view(request, id_proyecto):
    """
    Permite listar todas las fases registradas en el sistema, junto con las 
    operaciones de agregacion de fase.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fases = Fase.objects.all()
    ctx = {'proyecto':proyecto, 'fases':fases}
    return render_to_response('proyecto/agregar_fase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar fase a proyecto")
@miembro_proyecto()
def confirmacion_proyecto_agregar_fase_view(request, id_proyecto, id_fase):
    """
    Permite agregar una fase previamente seleccionada a un proyecto existente en el 
    sistema.
    """
    valido_uno = False
    valido_dos = False
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = Fase.objects.get(id=id_fase)
    try:
        phase = proyecto.fases.get(id=id_fase)
    except Fase.DoesNotExist:
        valido_uno = True
    try:
        project = fase.proyecto
    except Proyecto.DoesNotExist:
        valido_dos = True
    if fase.proyecto == None:
        valido_dos = True      
    if valido_uno and valido_dos:
        proyecto.fases.add(fase)
        proyecto.save()
    ctx = {'proyecto':proyecto, 'fase':fase, 'valido_uno':valido_uno, 'valido_dos':valido_dos}
    return render_to_response('proyecto/confirmacion_agregar_fase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Quitar fase de proyecto")
@miembro_proyecto()
def proyecto_quitar_fase_view(request, id_proyecto, id_fase):
    """
    Permite quitar una fase previamente seleccionada de un proyecto existente en el 
    sistema.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = Fase.objects.get(id=id_fase)
    fase.proyecto = None
    fase.save()
    proyecto.save()
    ctx = {'proyecto':proyecto, 'fase':fase}
    return render_to_response('proyecto/quitar_fase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar roles de proyecto")
@miembro_proyecto()
def roles_proyecto_view(request, id_proyecto):
    """
    Permite listar todos los roles pertenecientes a un proyecto existente en el sistema, 
    junto con las operaciones de agregacion de roles y eliminacion de roles.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    roles = Rol.objects.filter(roles_proyecto__id=id_proyecto)
    ctx = {'proyecto':proyecto, 'roles':roles}
    return render_to_response('proyecto/roles_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def proyecto_agregar_rol_view(request, id_proyecto):
    """
    Permite listar todos los roles registrados en el sistema, junto con las 
    operaciones de agregacion de rol.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    roles = Rol.objects.all()
    ctx = {'proyecto':proyecto, 'roles':roles}
    return render_to_response('proyecto/agregar_rol.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar rol a proyecto")
@miembro_proyecto()
def confirmacion_proyecto_agregar_rol_view(request, id_proyecto, id_rol):
    """
    Permite agregar un rol previamente seleccionado a un proyecto existente en el 
    sistema.
    """
    valido = False
    proyecto = Proyecto.objects.get(id=id_proyecto)
    rol = Rol.objects.get(id=id_rol)
    try:
        role = proyecto.roles.get(id=id_rol)
    except Rol.DoesNotExist:
        valido = True      
    if valido:
        proyecto.roles.add(rol)
        proyecto.save()
    ctx = {'proyecto':proyecto, 'rol':rol, 'valido':valido}
    return render_to_response('proyecto/confirmacion_agregar_rol.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Quitar rol de proyecto")
@miembro_proyecto()
def proyecto_quitar_rol_view(request, id_proyecto, id_rol):
    """
    Permite quitar un rol previamente seleccionado de un proyecto existente en el 
    sistema.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    rol = Rol.objects.get(id=id_rol)
    proyecto.roles.remove(rol)
    proyecto.save()
    ctx = {'proyecto':proyecto, 'rol':rol}
    return render_to_response('proyecto/quitar_rol.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar comite de proyecto")
@miembro_proyecto()
def comite_proyecto_view(request, id_proyecto):
    """
    Permite listar todos los miembros del comite de cambios perteneciente a un proyecto existente en el sistema, 
    junto con las operaciones de agregacion de miembros y eliminacion de miembros.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    miembros = User.objects.filter(comite_de_cambios_proyecto__id=id_proyecto)
    ctx = {'proyecto':proyecto, 'miembros':miembros}
    return render_to_response('proyecto/comite_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def proyecto_agregar_miembro_view(request, id_proyecto):
    """
    Permite listar todos los usuarios registrados en el sistema, junto con las 
    operaciones de agregacion de usuario.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    usuarios = User.objects.all()
    ctx = {'proyecto':proyecto, 'usuarios':usuarios}
    return render_to_response('proyecto/agregar_miembro.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar miembro a comite")
@miembro_proyecto()
def confirmacion_proyecto_agregar_miembro_view(request, id_proyecto, id_usuario):
    """
    Permite agregar un usuario previamente seleccionado al comite de cambios de un proyecto existente en el 
    sistema.
    """
    valido = False
    proyecto = Proyecto.objects.get(id=id_proyecto)
    usuario = User.objects.get(id=id_usuario)
    try:
        user = proyecto.comite_de_cambios.get(id=id_usuario)
    except User.DoesNotExist:
        valido = True      
    if valido:
        proyecto.comite_de_cambios.add(usuario)
        proyecto.save()
    ctx = {'proyecto':proyecto, 'usuario':usuario, 'valido':valido}
    return render_to_response('proyecto/confirmacion_agregar_miembro.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Quitar miembro de comite")
@miembro_proyecto()
def proyecto_quitar_miembro_view(request, id_proyecto, id_usuario):
    """
    Permite quitar un usuario previamente seleccionado del comite de cambios de un proyecto existente en el 
    sistema.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    usuario = User.objects.get(id=id_usuario)
    proyecto.comite_de_cambios.remove(usuario)
    proyecto.save()
    ctx = {'proyecto':proyecto, 'usuario':usuario}
    return render_to_response('proyecto/quitar_miembro.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Iniciar proyecto")
@miembro_proyecto()
def iniciar_proyecto_view(request, id_proyecto):
    """
    Permite arrancar un proyecto si es que se cumplen todas las condiciones mencionadas abajo:
        - El proyecto debe estar en estado Inactivo.
        - El proyecto debe poseer un lider.
        - El proyecto debe poseer al menos un miembro en su comite de cambios.
        - El proyecto debe poseer al menos una fase.
        - El proyecto debe poseer al menos un rol.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    inicio_valido = True
    estado_valido = True
    comite_valido = True
    fases_valido = True
    roles_valido = True
    
    if proyecto.estado != 0:
        estado_valido = False
        inicio_valido = False
    if proyecto.usuario_lider:
        lider_valido = True
    else:
        lider_valido = False
        inicio_valido = False
    if proyecto.comite_de_cambios.count() == 0:
        comite_valido = False
        inicio_valido = False
    if proyecto.fases.count() == 0:
        fases_valido = False
        inicio_valido = False
    if proyecto.roles.count() == 0:
        roles_valido = False
        inicio_valido = False
    
    if inicio_valido:
        proyecto.estado = 1
        proyecto.save()
        ctx = {'proyecto':proyecto, 'inicio_valido':inicio_valido, 'estado_valido':estado_valido, 'lider_valido':lider_valido, 'comite_valido':comite_valido, 'fases_valido':fases_valido, 'roles_valido':roles_valido}
        return render_to_response('proyecto/iniciar_proyecto.html', ctx, context_instance=RequestContext(request))
    else:
        ctx = {'proyecto':proyecto, 'inicio_valido':inicio_valido, 'estado_valido':estado_valido, 'lider_valido':lider_valido, 'comite_valido':comite_valido, 'fases_valido':fases_valido, 'roles_valido':roles_valido}
        return render_to_response('proyecto/iniciar_proyecto.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
def gestion_fases_view(request):
    """
    La vista del listado de fases del sistema. Para acceder a esta vista se deben cumplir los siguientes
    requisitos:
    - El usuario debe estar logueado.
    Esta vista permite al usuario listar y conocer las opciones de las fases del sistema.
    Inicialmente, se verifican los permisos del usuario solicitante para restringir (si es necesario) 
    los botones de accion sobre cada fase.
    La vista recibe los siguientes parametros:
    - request: contiene informacion sobre la sesion actual.
    La vista retorna lo siguiente:
    - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    crear_fase = False
    modificar_fase = False
    eliminar_fase = False
    visualizar_fase = False
    gestionar_roles = False
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
            elif p.nombre == 'Gestionar roles de fase':
                gestionar_roles = True
                
            if crear_fase and modificar_fase and eliminar_fase and visualizar_fase and gestionar_roles:
                break
        if crear_fase and modificar_fase and eliminar_fase and visualizar_fase and gestionar_roles:
                break
            
    fases = Fase.objects.all()
    ctx = {'fases':fases, 'crear_fase':crear_fase, 'modificar_fase':modificar_fase, 'eliminar_fase':eliminar_fase, 'visualizar_fase':visualizar_fase, 'gestionar_roles':gestionar_roles}
    return render_to_response('fase/gestion_fases.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear fase")
def crear_fase_view(request):
    """
    La vista para crear una fase. Para acceder a esta vista se deben cumplir los siguientes
    requisitos:
    - El usuario debe estar logueado.
    - El usuario debe poseer el permiso: Crear fase.
    Esta vista permite al usuario crear una fase en el sistema, para lograr esto, se verifica la validez de cada campo ingresado 
    y luego se crea la fase de acuerdo a los campos ingresados. 
    La vista recibe los siguientes parametros:
    - request: contiene informacion sobre la sesion actual.
    La vista retorna lo siguiente:
    - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
    generado en la vista, al template correspondiente.
    - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de fases. 
    """
    form = CrearFaseForm()
    if request.method == "POST":
        form = CrearFaseForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            duracion = form.cleaned_data['duracion']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            
            fase = Fase.objects.create(nombre=nombre, descripcion=descripcion, duracion=duracion, fecha_inicio=fecha_inicio)
            fase.save()
            return HttpResponseRedirect('/administracion/gestion_fases/')
            
        else:
            ctx = {'form':form}
            return render_to_response('fase/crear_fase.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('fase/crear_fase.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Modificar fase")
@fase_miembro_proyecto()
def modificar_fase_view(request, id_fase):
    """
    La vista para modificar una fase. Para acceder a esta vista se deben cumplir los siguientes
    requisitos:
    - El usuario debe estar logueado.
    - El usuario debe poseer el permiso: Modificar item.
    - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
    Esta vista permite al usuario modificar una fase previamente seleccionada, para lograr esto, 
    se verifica la validez de cada campo modificado y luego se guarda la fase de acuerdo a los campos ingresados.
    La vista recibe los siguientes parametros:
    - request: contiene informacion sobre la sesion actual.
    - id_fase: el identificador de la fase.
    La vista retorna lo siguiente:
    - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
    generado en la vista, al template correspondiente.
    - HttpResponseRedirect: si la operacion resulto valida, se redirige al template de visualizacion de la fase modificada. 
    """
    fase = Fase.objects.get(id=id_fase)
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
            return HttpResponseRedirect('/administracion/gestion_fases/fase/%s'%fase.id)
            
    if request.method == "GET":
        form = ModificarFaseForm(initial={
            'nombre': fase.nombre,
            'descripcion': fase.descripcion,
            'presupuesto': fase.duracion,
            })
    ctx = {'form': form, 'fase': fase}
    return render_to_response('fase/modificar_fase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Eliminar fase")
@fase_miembro_proyecto()
def eliminar_fase_view(request, id_fase):
    """
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
    La vista retorna lo siguiente:
    - render_to_response: si la operacion resulto ser de tipo GET o no se cumplieron las condiciones para eliminar, devuelve el contexto, 
    generado en la vista, al template correspondiente.
    - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de fases. 
    """
    fase = Fase.objects.get(id=id_fase)
    valido = True
    if fase.estado == 2 or fase.estado == 1:
        valido = False
    if request.method == "POST":
        if valido == True:
            fase.delete()
            return HttpResponseRedirect('/administracion/gestion_fases/')
        else:
            ctx = {'fase':fase, 'valido':valido}
            return render_to_response('fase/eliminar_fase.html', ctx, context_instance=RequestContext(request))
    if request.method == "GET":
        ctx = {'fase':fase, 'valido':valido}
        return render_to_response('fase/eliminar_fase.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Visualizar fase")
@fase_miembro_proyecto()
def visualizar_fase_view(request, id_fase):
    """
    La vista para visualizar una fase. Para acceder a esta vista se deben cumplir los siguientes
    requisitos:
    - El usuario debe estar logueado.
    - El usuario debe poseer el permiso: Visualizar fase.
    - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
    Esta vista permite al usuario visualizar todos los campos guardados de una fase previamente seleccionada.
    La vista recibe los siguientes parametros:
    - request: contiene informacion sobre la sesion actual.
    - id_fase: el identificador de la fase.
    La vista retorna lo siguiente:
    - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente.
    """
    fase = Fase.objects.get(id=id_fase)
    ctx = {'fase': fase}
    return render_to_response('fase/visualizar_fase.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar roles de fase")
@fase_miembro_proyecto()
def roles_fase_view(request, id_fase):
    """
    La vista del listado de roles por fase. Para acceder a esta vista se deben cumplir los siguientes
    requisitos:
    - El usuario debe estar logueado.
    - El usuario debe poseer el permiso: Gestionar roles de fase.
    - El usuario debe ser miembro del proyecto al cual esta ligada la fase.
    Esta vista permite al usuario listar y conocer las opciones de los roles de la fase previamente seleccionada.
    La vista recibe los siguientes parametros:
    - request: contiene informacion sobre la sesion actual.
    - id_fase: el identificador de la fase.
    La vista retorna lo siguiente:
    - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    fase = Fase.objects.get(id=id_fase)
    roles = Rol.objects.filter(fase__id=id_fase)
    ctx = {'fase':fase, 'roles':roles}
    return render_to_response('fase/roles_fase.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
def fase_agregar_rol_view(request, id_fase):
    """
    La vista del listado de roles del proyecto ligado a la fase. Para acceder a esta vista se deben cumplir los siguientes
    requisitos:
    - El usuario debe estar logueado.
    Esta vista permite al usuario listar todos los roles del proyecto al cual esta ligada la fase, ademas, el template relacionado concede 
    las opciones para agregar un rol seleccionado.
    La vista recibe los siguientes parametros:
    - request: contiene informacion sobre la sesion actual.
    - id_fase: el identificador de la fase.
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
def confirmacion_fase_agregar_rol_view(request, id_fase, id_rol):
    """
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
    La vista retorna lo siguiente:
    - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    valido = False
    fase = Fase.objects.get(id=id_fase)
    rol = Rol.objects.get(id=id_rol)
    try:
        role = fase.roles.get(id=id_rol)
    except Rol.DoesNotExist:
        valido = True      
    if valido:
        fase.roles.add(rol)
        fase.save()
    ctx = {'fase':fase, 'rol':rol, 'valido':valido}
    return render_to_response('fase/confirmacion_agregar_rol.html', ctx, context_instance=RequestContext(request))  
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Quitar rol de fase")
@fase_miembro_proyecto()
def fase_quitar_rol_view(request, id_fase, id_rol):
    """
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
    rol = Rol.objects.get(id=id_rol)
    fase.roles.remove(rol)
    fase.save()
    ctx = {'fase':fase, 'rol':rol}
    return render_to_response('fase/quitar_rol.html', ctx, context_instance=RequestContext(request))
  
@login_required(login_url='/login/')
def gestion_tipos_item_view(request):
    """
    Permite listar todos los tipos de item registrados en el sistema, junto con las 
    operaciones disponibles por cada tipo de item.
    """
    tipos_item = TipoItem.objects.all()
    ctx = {'tipos_item': tipos_item}
    return render_to_response('tipo_item/gestion_tipos_item.html', ctx, context_instance=RequestContext(request))
  
@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear tipo de item")
def crear_tipo_item_view(request):
    """
    Permite crear un nuevo tipo de item en el sistema.
    """
    form = CrearTipoItemForm()
    if request.method == "POST":
        form = CrearTipoItemForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            
            tipo_item = TipoItem.objects.create(nombre=nombre, descripcion=descripcion)
            tipo_item.save()
            return HttpResponseRedirect('/administracion/gestion_tipos_item/')
            
        else:
            ctx = {'form':form}
            return render_to_response('tipo_item/crear_tipo_item.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('tipo_item/crear_tipo_item.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Modificar tipo de item")
def modificar_tipo_item_view(request, id_tipo_item):

    tipo_item = TipoItem.objects.get(id=id_tipo_item)
    if request.method == "POST":
        form = ModificarTipoItemForm(data=request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            
            tipo_item.nombre = nombre
            tipo_item.descripcion = descripcion

            tipo_item.save()
            return HttpResponseRedirect('/administracion/gestion_tipos_item/tipo_item/%s'%tipo_item.id)
            
    if request.method == "GET":
        form = ModificarTipoItemForm(initial={
            'nombre': tipo_item.nombre,
            'descripcion': tipo_item.descripcion,
            })
    ctx = {'form': form, 'tipo_item': tipo_item}
    return render_to_response('tipo_item/modificar_tipo_item.html', ctx, context_instance=RequestContext(request))
  
@login_required(login_url='/login/')
@permiso_requerido(permiso="Visualizar tipo de item")
def visualizar_tipo_item_view(request, id_tipo_item):

    tipo_item = TipoItem.objects.get(id=id_tipo_item)
    ctx = {'tipo_item': tipo_item}
    return render_to_response('tipo_item/visualizar_tipo_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Eliminar tipo de item")
def eliminar_tipo_item_view(request, id_tipo_item):
    """
    Permite eliminar un tipo de item existente en el sistema.
    """
    tipo_item = TipoItem.objects.get(id=id_tipo_item)
    if request.method == "POST":
        TipoItem.objects.get(id=id_tipo_item).delete()
        return HttpResponseRedirect('/administracion/gestion_tipos_item/')
    if request.method == "GET":
        ctx = {'tipo_item':tipo_item}
        return render_to_response('tipo_item/eliminar_tipo_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar tipos de atributo de tipo de item")

def tipos_atributo_tipo_item_view(request, id_tipo_item):
    id_tipoitem=id_tipo_item
    tipo_item = TipoItem.objects.get(id=id_tipo_item)
    tipos_atributo = TipoAtributo.objects.filter(tipoitem__id=id_tipoitem)
    ctx = {'tipo_item':tipo_item, 'tipos_atributo':tipos_atributo}
    return render_to_response('tipo_item/tipos_atributo_tipo_item.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def agregar_tipo_atributo_view(request, id_tipo_item):
    """

    """
    tipo_item = TipoItem.objects.get(id=id_tipo_item)
    tipos_atributo = TipoAtributo.objects.all()
    ctx = {'tipo_item':tipo_item, 'tipos_atributo':tipos_atributo}
    return render_to_response('tipo_item/agregar_tipo_atributo.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar tipo de atributo a tipo de item")
def confirmacion_agregar_tipo_atributo_view(request, id_tipo_item, id_tipo_atributo):
    """
    Permite agregar un tipo de atributo previamente seleccionado a un tipo de item existente en el 
    sistema.
    """
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
    ctx = {'tipo_item':tipo_item, 'tipo_atributo':tipo_atributo, 'valido':valido}
    return render_to_response('tipo_item/confirmacion_agregar_tipo_atributo.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Quitar tipo atributo de tipo de item")
def quitar_tipo_atributo_view(request, id_tipo_item, id_tipo_atributo):
    """
    Permite quitar un tipo de atributo previamente seleccionado de un tipo de item existente en el 
    sistema.
    """
    tipo_item = TipoItem.objects.get(id=id_tipo_item)
    tipo_atributo = TipoAtributo.objects.get(id=id_tipo_atributo)
    atributos = ValorAtributo.objects.filter(tipo_atributo__id=id_tipo_atributo)
    valido = True
    if atributos:
        valido = False
    if valido:
        tipo_item.tipos_atributo.remove(tipo_atributo)
        tipo_item.save()
    ctx = {'tipo_item':tipo_item, 'tipo_atributo':tipo_atributo, 'valido':valido}
    return render_to_response('tipo_item/quitar_tipo_atributo.html', ctx, context_instance=RequestContext(request))