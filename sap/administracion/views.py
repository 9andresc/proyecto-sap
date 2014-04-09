from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from administracion.forms import CrearUsuarioForm, ModificarUsuarioForm
from administracion.models import Rol

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
        form = CrearUsuarioForm(request.POST)
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
            password_uno = form.cleaned_data['password_uno']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']
            usuario.username = username
            usuario.email = email
            usuario.set_password(password_uno)
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
    junto con las operaciones de agregacion de roles y eliminación de roles.
    """
    usuario = User.objects.get(id=id_usuario)
    roles = Rol.objects.filter(user__id=id_usuario)
    ctx = {'usuario':usuario, 'roles':roles}
    return render_to_response('usuario/roles_usuario.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def agregar_rol_view(request, id_usuario):
    """
    Permite listar todos los roles registrados en el sistema, junto con las 
    operaciones de agregación de rol.
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
    valido = True
    usuario = User.objects.get(id=id_usuario)
    rol = Rol.objects.get(id=id_rol)
    if usuario.roles.get(id=id_rol) == rol:
        valido = False
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