from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from administracion.forms import CrearUsuarioForm, ModificarUsuarioForm, CambiarContrasenhaForm, CrearRolForm, ModificarRolForm, CrearTipoAtributoForm, ModificarTipoAtributoForm
from administracion.models import Rol, Permiso, TipoAtributo, TIPO_DATO

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
def visualizar_usuario_view(request, id_usuario):
    """
    Permite visualizar todos los campos de un usuario existente en el sistema.
    """
    usuario = User.objects.get(id=id_usuario)
    ctx = {'usuario': usuario}
    return render_to_response('usuario/visualizar_usuario.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
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
def visualizar_rol_view(request, id_rol):
    """
    Permite visualizar todos los campos de un rol existente en el sistema.
    """
    rol = Rol.objects.get(id=id_rol)
    ctx = {'rol': rol}
    return render_to_response('rol/visualizar_rol.html', ctx, context_instance=RequestContext(request)) 
    
@login_required(login_url='/login/')
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
def modificar_tipo_atributo_view(request, id_tipo_atributo):
    """
    Permite modificar un tipo atributo existente en el sistema.
    """
    tipo_atributo = TipoAtributo.objects.get(id=id_tipo_atributo)
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
    ctx = {'form': form, 'tipo_atributo': tipo_atributo}
    return render_to_response('tipo_atributo/modificar_tipo_atributo.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def eliminar_tipo_atributo_view(request, id_tipo_atributo):
    """
    Permite eliminar un tipo atributo existente en el sistema.
    """
    tipo_atributo = TipoAtributo.objects.get(id=id_tipo_atributo)
    if request.method == "POST":
        TipoAtributo.objects.get(id=id_tipo_atributo).delete()
        return HttpResponseRedirect('/administracion/gestion_tipos_atributo/')
    if request.method == "GET":
        ctx = {'tipo_atributo':tipo_atributo}
        return render_to_response('tipo_atributo/eliminar_tipo_atributo.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def visualizar_tipo_atributo_view(request, id_tipo_atributo):
    """
    Permite visualizar todos los campos de un tipo atributo existente en el sistema.
    """
    tipo_atributo = TipoAtributo.objects.get(id=id_tipo_atributo)
    ctx = {'tipo_atributo': tipo_atributo}
    return render_to_response('tipo_atributo/visualizar_tipo_atributo.html', ctx, context_instance=RequestContext(request))
