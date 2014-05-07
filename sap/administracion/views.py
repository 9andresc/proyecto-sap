from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from administracion.forms import CrearUsuarioForm, ModificarUsuarioForm, CambiarContrasenhaForm, CrearRolForm, ModificarRolForm, CrearTipoAtributoForm, ModificarTipoAtributoForm, CrearProyectoForm, ModificarProyectoForm
from administracion.models import Rol, Permiso, TipoAtributo, Proyecto
from desarrollo.models import ValorAtributo
from inicio.decorators import permiso_requerido, miembro_proyecto

@login_required(login_url='/login/')
def gestion_usuarios_view(request):
    """
    ::
    
        La vista del listado de usuarios del sistema. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
                - El usuario debe estar logueado.
                Esta vista permite al usuario listar y conocer las opciones de los usuarios del sistema.
                Inicialmente, se verifican los permisos del usuario solicitante para restringir (si es necesario) 
                los botones de accion sobre cada usuario.
                
        La vista recibe los siguientes parametros:
    
                - request: contiene informacion sobre la sesion actual.
            
        La vista retorna lo siguiente:
        
                - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    crear_usuario = False
    modificar_usuario = False
    eliminar_usuario = False
    visualizar_usuario = False
    gestionar_roles = False
    roles = request.user.roles.all()
    for r in roles:
        for p in r.permisos.all():
            if p.nombre == 'Crear usuario':
                crear_usuario = True
            elif p.nombre == 'Modificar usuario':
                modificar_usuario = True
            elif p.nombre == 'Eliminar usuario':
                eliminar_usuario = True
            elif p.nombre == 'Visualizar usuario':
                visualizar_usuario = True
            elif p.nombre == 'Gestionar roles de usuario':
                gestionar_roles = True
                
            if crear_usuario and modificar_usuario and eliminar_usuario and visualizar_usuario and gestionar_roles:
                break
        if crear_usuario and modificar_usuario and eliminar_usuario and visualizar_usuario and gestionar_roles:
                break
            
    usuarios = User.objects.all()
    ctx = {'usuarios':usuarios, 'crear_usuario':crear_usuario, 'modificar_usuario':modificar_usuario, 'eliminar_usuario':eliminar_usuario, 'visualizar_usuario':visualizar_usuario, 'gestionar_roles':gestionar_roles}
    return render_to_response('usuario/gestion_usuarios.html', ctx, context_instance=RequestContext(request))
   
@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear usuario")
def crear_usuario_view(request):
    """
    ::
    
        La vista para crear un usuario. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Crear usuario.
            
        Esta vista permite al usuario crear un usuario para lograr esto, se verifica la validez de cada campo ingresado y 
        luego se crea el usuario de acuerdo a los campos ingresados. 
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de usuarios. 
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
    ::
    
        La vista para modificar un usuario. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Modificar usuario.
            
        Esta vista permite al usuario modificar un usuario previamente seleccionado, para lograr esto, 
        se verifica la validez de cada campo modificado y luego se guarda el usuario de acuerdo a los campos ingresados.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_usuario: el identificador del usuario.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template de visualizacion del usuario modificada. 
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
    """
    ::
    
        La vista para cambiar la contrasenha de un usuario. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Cambiar contrasenha.
            
        Esta vista permite al usuario cambiar su contrasenha una vez logueado, para lograr esto, 
        se verifica la validez de cada campo modificado y luego se guarda la contrasenha de acuerdo a los campos ingresados.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_usuario: el identificador del usuario.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template de visualizacion del usuario modificada. 
    """
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
    ::
    
        La vista para eliminar un usuario. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Eliminar usuario.
            
        Esta vista permite al usuario eliminar un usuario previamente seleccionado.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_usuario: el identificador del usuario.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o no se cumplieron las condiciones para eliminar, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de fases. 
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
    ::
    
        La vista para visualizar un usuario. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Visualizar usuario.
            
        Esta vista permite al usuario visualizar todos los campos guardados de un usuario previamente seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_usuario: el identificador del usuario.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente.
    """
    usuario = User.objects.get(id=id_usuario)
    ctx = {'usuario': usuario}
    return render_to_response('usuario/visualizar_usuario.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar roles de usuario")
def roles_usuario_view(request, id_usuario):
    """
    ::
    
        La vista del listado de roles por usuario. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Gestionar roles de usuario.
            
        Esta vista permite al usuario listar y conocer las opciones de los roles del usuario previamente seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_usuario: el identificador del usuario.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    usuario = User.objects.get(id=id_usuario)
    roles = Rol.objects.filter(user__id=id_usuario)
    ctx = {'usuario':usuario, 'roles':roles}
    return render_to_response('usuario/roles_usuario.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def usuario_agregar_rol_view(request, id_usuario):
    """
    ::
    
        La vista del listado de roles ligados al usuario. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            
        Esta vista permite al usuario listar todos los roles sistema, ademas, el template relacionado concede 
        las opciones para agregar un rol seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_usuario: el identificador del usuario.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    usuario = User.objects.get(id=id_usuario)
    roles = Rol.objects.all()
    ctx = {'usuario':usuario, 'roles':roles}
    return render_to_response('usuario/agregar_rol.html', ctx, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar rol a usuario")
def usuario_confirmacion_agregar_rol_view(request, id_rol, id_usuario):
    """
    ::
    
        La vista de confirmacion de agregacion de un rol a un usuario. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Agregar rol a usuario.
            
        Esta vista permite al usuario agregar un rol seleccionado a el usuario seleccionado previamente. Se verifica si el rol a agregar ya 
        pertenece al usuario, en cuyo caso se cancelara la operacion.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_usuario: el identificador del usuario.
            - id_rol: el identificador del rol.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
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
def usuario_quitar_rol_view(request, id_rol, id_usuario):
    """
    ::
    
        La vista para quitar un rol de un usuario. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Quitar rol de usuario.
        
        Esta vista permite al usuario quitar un rol seleccionado de un usuario seleccionado previamente.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_usuario: el identificador de la usuario.
            - id_rol: el identificador del rol.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
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
    ::
    
        La vista del listado de roles del sistema. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
                - El usuario debe estar logueado.
                Esta vista permite al usuario listar y conocer las opciones de los roles del sistema.
                Inicialmente, se verifican los permisos del usuario solicitante para restringir (si es necesario) 
                los botones de accion sobre cada rol.
                
        La vista recibe los siguientes parametros:
    
                - request: contiene informacion sobre la sesion actual.
            
        La vista retorna lo siguiente:
        
                - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    crear_rol = False
    modificar_rol = False
    eliminar_rol = False
    visualizar_rol = False
    gestionar_permisos= False
    roles = request.user.roles.all()
    for r in roles:
        for p in r.permisos.all():
            if p.nombre == 'Crear rol':
                crear_rol = True
            elif p.nombre == 'Modificar rol':
                modificar_rol = True
            elif p.nombre == 'Eliminar rol':
                eliminar_rol = True
            elif p.nombre == 'Visualizar rol':
                visualizar_rol = True
            elif p.nombre == 'Gestionar permisos de rol':
                gestionar_permisos = True    
                
            if crear_rol and modificar_rol and eliminar_rol and visualizar_rol and gestionar_permisos:
                break
        if crear_rol and modificar_rol and eliminar_rol and visualizar_rol and gestionar_permisos:
                break
            
    roles = Rol.objects.all()
    ctx = {'roles':roles, 'crear_rol':crear_rol, 'modificar_rol':modificar_rol, 'eliminar_rol':eliminar_rol, 'visualizar_rol':visualizar_rol, 'gestionar_permisos':gestionar_permisos}
    return render_to_response('rol/gestion_roles.html', ctx, context_instance=RequestContext(request))   
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear rol")
def crear_rol_view(request):
    """
    ::
    
        La vista para crear un rol. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Crear rol.
            
        Esta vista permite al usuario crear un rol para lograr esto, se verifica la validez de cada campo ingresado y 
        luego se crea el rol de acuerdo a los campos ingresados. 
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de usuarios. 
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
    ::
    
        La vista para modificar un rol. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Modificar rol.
            
        Esta vista permite al usuario modificar un rol previamente seleccionado, para lograr esto, 
        se verifica la validez de cada campo modificado y luego se guarda el rol de acuerdo a los campos ingresados.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_rol: el identificador del rol.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template de visualizacion del usuario modificada. 
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
    ::
    
        La vista para eliminar un rol. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Eliminar rol.
            
        Esta vista permite al usuario eliminar un rol previamente seleccionado.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_rol: el identificador del rol.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o no se cumplieron las condiciones para eliminar, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de fases. 
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
    ::
    
        La vista para visualizar un rol. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Visualizar rol.
            
        Esta vista permite al usuario visualizar todos los campos guardados de un rol previamente seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_rol: el identificador del rol.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente.
    """
    rol = Rol.objects.get(id=id_rol)
    ctx = {'rol': rol}
    return render_to_response('rol/visualizar_rol.html', ctx, context_instance=RequestContext(request)) 
    
@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar permisos de rol")
def permisos_rol_view(request, id_rol):
    """
    ::
    
        La vista del listado de permisos por rol. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Gestionar permisos de rol.
            
        Esta vista permite al usuario listar y conocer las opciones de los permisos del rol previamente seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_rol: el identificador del rol.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    rol = Rol.objects.get(id=id_rol)
    permisos = Permiso.objects.filter(rol__id=id_rol)
    ctx = {'rol':rol, 'permisos':permisos}
    return render_to_response('rol/permisos_rol.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def agregar_permiso_view(request, id_rol):
    """
    ::
    
        La vista del listado de permisos ligados al rol. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            
        Esta vista permite al usuario listar todos los permisos del sistema, ademas, el template relacionado concede 
        las opciones para agregar un permiso seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_rol: el identificador del rol.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    rol = Rol.objects.get(id=id_rol)
    permisos = Permiso.objects.all()
    ctx = {'rol':rol, 'permisos':permisos}
    return render_to_response('rol/agregar_permiso.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar permiso a rol")
def confirmacion_agregar_permiso_view(request, id_permiso, id_rol):
    """
    ::
    
        La vista de confirmacion de agregacion de un permiso a un rol. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Agregar permiso a rol.
            
        Esta vista permite al usuario agregar un permiso seleccionado a el rol seleccionado previamente. Se verifica si el permiso a agregar ya 
        pertenece al rol, en cuyo caso se cancelara la operacion.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_rol: el identificador del rol.
            - id_permiso: el identificador del permiso.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
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
def quitar_permiso_view(request, id_permiso, id_rol):
    """
    ::
    
        La vista para quitar un permiso de un rol. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Quitar permiso de rol.
        
        Esta vista permite al usuario quitar un permiso seleccionado de un rol seleccionado previamente.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_rol: el identificador de la rol.
            - id_permiso: el identificador del permiso.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
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
    ::
    
        La vista del listado de tipos de atributo del sistema. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
                - El usuario debe estar logueado.
                Esta vista permite al usuario listar y conocer las opciones de los tipos de atributo del sistema.
                Inicialmente, se verifican los permisos del usuario solicitante para restringir (si es necesario) 
                los botones de accion sobre cada tipo de atributo.
                
        La vista recibe los siguientes parametros:
    
                - request: contiene informacion sobre la sesion actual.
            
        La vista retorna lo siguiente:
        
                - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    crear_tipo_de_atributo = False
    modificar_tipo_de_atributo = False
    eliminar_tipo_de_atributo = False
    visualizar_tipo_de_atributo = False
    roles = request.user.roles.all()
    for r in roles:
        for p in r.permisos.all():
            if p.nombre == 'Crear tipo de atributo':
                crear_tipo_de_atributo = True
            elif p.nombre == 'Modificar tipo de atributo':
                modificar_tipo_de_atributo = True
            elif p.nombre == 'Eliminar tipo de atributo':
                eliminar_tipo_de_atributo = True
            elif p.nombre == 'Visualizar tipo de atributo':
                visualizar_tipo_de_atributo = True
                
            if crear_tipo_de_atributo and modificar_tipo_de_atributo and eliminar_tipo_de_atributo and visualizar_tipo_de_atributo:
                break
        if crear_tipo_de_atributo and modificar_tipo_de_atributo and eliminar_tipo_de_atributo and visualizar_tipo_de_atributo:
                break
            
    tipos_atributo = TipoAtributo.objects.all()
    ctx = {'tipos_atributo':tipos_atributo, 'crear_tipo_de_atributo':crear_tipo_de_atributo, 'modificar_tipo_de_atributo':modificar_tipo_de_atributo, 'eliminar_tipo_de_atributo':eliminar_tipo_de_atributo, 'visualizar_tipo_de_atributo':visualizar_tipo_de_atributo}
    return render_to_response('tipo_atributo/gestion_tipos_atributo.html', ctx, context_instance=RequestContext(request))  
  
@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear tipo de atributo")
def crear_tipo_atributo_view(request):
    """
    ::
    
        La vista para crear un tipo de atributo. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Crear tipo de atributo.
            
        Esta vista permite al usuario crear un tipo de atributo para lograr esto, se verifica la validez de cada campo ingresado y 
        luego se crea el tipo de atributo de acuerdo a los campos ingresados. 
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de usuarios. 
    """
    form = CrearTipoAtributoForm()
    if request.method == "POST":
        form = CrearTipoAtributoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            tipo_dato = form.cleaned_data['tipo_dato']
            
            obligatorio = request.POST.get('obligatorio')
            if obligatorio == 0:
                obligatorio = False
            else:
                obligatorio = True
                
            if tipo_dato == 0:
                longitud = request.POST.get('longitud')
                precision = request.POST.get('precision')
                tipo_atributo = TipoAtributo.objects.create(nombre=nombre, descripcion=descripcion, tipo_dato=tipo_dato, longitud=longitud, precision=precision, obligatorio=obligatorio)
                tipo_atributo.save()
            elif tipo_dato == 1 or tipo_dato == 4:
                tipo_atributo = TipoAtributo.objects.create(nombre=nombre, descripcion=descripcion, tipo_dato=tipo_dato, obligatorio=obligatorio)
                tipo_atributo.save()
            else:
                longitud = request.POST.get('longitud')
                tipo_atributo = TipoAtributo.objects.create(nombre=nombre, descripcion=descripcion, tipo_dato=tipo_dato, longitud=longitud, obligatorio=obligatorio)
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
    ::
    
        La vista para modificar un tipo de atributo. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Modificar tipo de atributo.
            
        Esta vista permite al usuario modificar un tipo de atributo previamente seleccionada, para lograr esto, 
        se verifica la validez de cada campo modificado y luego se guarda el tipo de atributo de acuerdo a los campos ingresados.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_tipo_atributo: el identificador del tipo de atributo.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template de visualizacion del usuario modificada. 
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
            
            obligatorio = request.POST.get('obligatorio')
            if obligatorio == 0:
                obligatorio = False
            else:
                obligatorio = True
                
            if tipo_dato == 0:
                longitud = request.POST.get('longitud')
                precision = request.POST.get('precision')
                tipo_atributo.nombre = nombre
                tipo_atributo.descripcion = descripcion
                tipo_atributo.tipo_dato = tipo_dato
                tipo_atributo.longitud = longitud
                tipo_atributo.precision = precision
                tipo_atributo.obligatorio = obligatorio
                tipo_atributo.save()
            elif tipo_dato == 1 or tipo_dato == 4:
                tipo_atributo.nombre = nombre
                tipo_atributo.descripcion = descripcion
                tipo_atributo.tipo_dato = tipo_dato
                tipo_atributo.obligatorio = obligatorio
                tipo_atributo.save()
            else:
                longitud = request.POST.get('longitud')
                tipo_atributo.nombre = nombre
                tipo_atributo.descripcion = descripcion
                tipo_atributo.tipo_dato = tipo_dato
                tipo_atributo.longitud = longitud
                tipo_atributo.obligatorio = obligatorio
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
    ::
    
        La vista para eliminar un tipo de atributo. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Eliminar tipo de atributo.
            
        Esta vista permite al usuario eliminar un tipo de atributo previamente seleccionado.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_tipo_atributo: el identificador del tipo de atributo.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o no se cumplieron las condiciones para eliminar, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de fases. 
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
    ::
    
        La vista para visualizar un tipo de atributo. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Visualizar tipo de atributo.
            
        Esta vista permite al usuario visualizar todos los campos guardados de un tipo de atributo previamente seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_tipo_atributo: el identificador del tipo de atributo.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente.
    """
    tipo_atributo = TipoAtributo.objects.get(id=id_tipo_atributo)
    ctx = {'tipo_atributo': tipo_atributo}
    return render_to_response('tipo_atributo/visualizar_tipo_atributo.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def gestion_proyectos_view(request):
    """
    ::
    
        La vista del listado de proyectos del sistema. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
                - El usuario debe estar logueado.
                Esta vista permite al usuario listar y conocer las opciones de los proyectos del sistema.
                Inicialmente, se verifican los permisos del usuario solicitante para restringir (si es necesario) 
                los botones de accion sobre cada proyecto.
                
        La vista recibe los siguientes parametros:
    
                - request: contiene informacion sobre la sesion actual.
            
        La vista retorna lo siguiente:
        
                - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    crear_proyecto = False
    modificar_proyecto = False
    eliminar_proyecto = False
    visualizar_proyecto = False
    gestionar_usuarios = False
    gestionar_roles = False
    gestionar_comite = False
    iniciar_proyecto = False
    roles = request.user.roles.all()
    for r in roles:
        for p in r.permisos.all():
            if p.nombre == 'Crear proyecto':
                crear_proyecto = True
            elif p.nombre == 'Modificar proyecto':
                modificar_proyecto = True
            elif p.nombre == 'Eliminar proyecto':
                eliminar_proyecto = True
            elif p.nombre == 'Visualizar proyecto':
                visualizar_proyecto = True
            elif p.nombre == 'Gestionar usuarios de proyecto':
                gestionar_usuarios = True
            elif p.nombre == 'Gestionar comite de proyecto':
                gestionar_comite = True
            elif p.nombre == 'Gestionar roles de proyecto':
                gestionar_roles = True
            elif p.nombre == 'Iniciar proyecto':
                iniciar_proyecto = True
                    
            if crear_proyecto and modificar_proyecto and eliminar_proyecto and visualizar_proyecto and gestionar_usuarios and gestionar_roles and gestionar_comite and iniciar_proyecto:
                break
        if crear_proyecto and modificar_proyecto and eliminar_proyecto and visualizar_proyecto and gestionar_usuarios and gestionar_roles and gestionar_comite and iniciar_proyecto:
                break
            
    proyectos = Proyecto.objects.all()
    ctx = {'proyectos':proyectos, 'crear_proyecto':crear_proyecto, 'modificar_proyecto':modificar_proyecto, 'eliminar_proyecto':eliminar_proyecto, 'visualizar_proyecto':visualizar_proyecto,'gestionar_usuarios':gestionar_usuarios, 'gestionar_roles':gestionar_roles, 'gestionar_comite':gestionar_comite, 'iniciar_proyecto':iniciar_proyecto}
    return render_to_response('proyecto/gestion_proyectos.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear proyecto")
def crear_proyecto_view(request):
    """
    ::
    
        La vista para crear un proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Crear proyecto.
            
        Esta vista permite al usuario crear un proyecto para lograr esto, se verifica la validez de cada campo ingresado y 
        luego se crea el proyecto de acuerdo a los campos ingresados. 
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de usuarios. 
    """
    form = CrearProyectoForm()
    usuarios = User.objects.all()
    if request.method == "POST":
        form = CrearProyectoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            presupuesto = form.cleaned_data['presupuesto']
            complejidad = form.cleaned_data['complejidad']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            
            id_lider = request.POST.get('usuario_lider')
            
            lider = User.objects.get(id=id_lider)
            rol_lider = Rol.objects.get(nombre="Lider de proyecto")
            lider.roles.add(rol_lider)
            
            proyecto = Proyecto.objects.create(nombre=nombre, descripcion=descripcion, presupuesto=presupuesto, complejidad=complejidad, fecha_inicio=fecha_inicio, usuario_lider=lider)
            proyecto.roles.add(rol_lider)
            proyecto.usuarios.add(lider)
            proyecto.save()
            return HttpResponseRedirect('/administracion/gestion_proyectos/')
            
        else:
            ctx = {'form':form, 'usuarios':usuarios}
            return render_to_response('proyecto/crear_proyecto.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form, 'usuarios':usuarios}
    return render_to_response('proyecto/crear_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Modificar proyecto")
@miembro_proyecto()
def modificar_proyecto_view(request, id_proyecto):
    """
    ::
    
        La vista para modificar un proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Modificar proyecto.
            - El usuario debe ser miembro del proyecto que se quiere modificar.
            
        Esta vista permite al usuario modificar un proyecto previamente seleccionada, para lograr esto, 
        se verifica la validez de cada campo modificado y luego se guarda el proyecto de acuerdo a los campos ingresados.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o el formulario resulto invalido, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template de visualizacion de la fase modificada. 
    """
    usuarios = User.objects.all()
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if request.method == "POST":
        form = ModificarProyectoForm(data=request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            presupuesto = form.cleaned_data['presupuesto']
            complejidad = form.cleaned_data['complejidad']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            
            id_lider = request.POST.get('usuario_lider')
            
            lider = User.objects.get(id=id_lider)
            
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
    ctx = {'form': form, 'proyecto': proyecto, 'usuarios':usuarios}
    return render_to_response('proyecto/modificar_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Eliminar proyecto")
@miembro_proyecto()
def eliminar_proyecto_view(request, id_proyecto):
    """
    ::
    
        La vista para eliminar un proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Eliminar proyecto.
            - El usuario debe ser miembro del proyecto.
            
        Esta vista permite al usuario eliminar un proyecto previamente seleccionada, para lograr esto, 
        se verifica si el proyecto cumple las siguientes condiciones:
        
            - El proyecto debe estar en estado Finalizado.
            
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: si la operacion resulto ser de tipo GET o no se cumplieron las condiciones para eliminar, devuelve el contexto, 
            generado en la vista, al template correspondiente.
            - HttpResponseRedirect: si la operacion resulto valida, se redirige al template del listado de fases. 
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
    ::
    
        La vista para visualizar un proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Visualizar proyecto.
            - El usuario debe ser miembro del proyecto que desea visualizar.
            
        Esta vista permite al usuario visualizar todos los campos guardados de un proyecto previamente seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    ctx = {'proyecto': proyecto}
    return render_to_response('proyecto/visualizar_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar usuarios de proyecto")
@miembro_proyecto()
def usuarios_proyecto_view(request, id_proyecto):
    """
    ::
    
        La vista del listado de usuarios por proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Gestionar usuarios de proyecto.
            - El usuario debe ser miembro del proyecto.
            
        Esta vista permite al usuario listar y conocer las opciones de los usuarios que componen el proyecto previamente seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    usuarios = User.objects.filter(usuarios_proyecto__id=id_proyecto)
    ctx = {'proyecto':proyecto, 'usuarios':usuarios}
    return render_to_response('proyecto/usuarios_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def proyecto_agregar_usuario_view(request, id_proyecto):
    """
    ::
    
        La vista del listado de usuarios miembros del proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            
        Esta vista permite al usuario listar todos los usuarios miembros del proyecto, ademas, el template relacionado concede 
        las opciones para agregar un usuario seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    usuarios = User.objects.all()
    ctx = {'proyecto':proyecto, 'usuarios':usuarios}
    return render_to_response('proyecto/agregar_usuario.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar usuario a proyecto")
@miembro_proyecto()
def proyecto_confirmacion_agregar_usuario_view(request, id_proyecto, id_usuario):
    """
    ::
    
        La vista de confirmacion de agregacion de un usuario a un proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Agregar usuario a proyecto.
            - El usuario debe ser miembro del proyecto.
            
        Esta vista permite al usuario agregar un usuario seleccionado a un proyecto seleccionado previamente. Se verifica si el usuario a agregar ya 
        pertenece al proyecto, en cuyo caso se cancelara la operacion.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            - id_usuario: el identificador del usuario.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
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
    ::
    
        La vista para quitar un usuario de la lista de miembros de un proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Quitar usuario de proyecto.
            - El usuario debe pertenecer al proyecto.
            
        Esta vista permite al usuario quitar un usuario seleccionado de un proyecto seleccionado previamente.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador de la proyecto.
            - id_usuario: el identificador del usuario.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    usuario = User.objects.get(id=id_usuario)
    proyecto.usuarios.remove(usuario)
    proyecto.save()
    ctx = {'proyecto':proyecto, 'usuario':usuario}
    return render_to_response('proyecto/quitar_usuario.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar roles de proyecto")
@miembro_proyecto()
def roles_proyecto_view(request, id_proyecto):
    """
    ::
    
        La vista del listado de roles por proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Gestionar roles de proyecto.
            - El usuario debe ser miembro del proyecto.
            
        Esta vista permite al usuario listar y conocer las opciones de los roles del proyecto previamente seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    roles = Rol.objects.filter(roles_proyecto__id=id_proyecto)
    ctx = {'proyecto':proyecto, 'roles':roles}
    return render_to_response('proyecto/roles_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def proyecto_agregar_rol_view(request, id_proyecto):
    """
    ::
    
        La vista del listado de roles ligados al proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            
        Esta vista permite al usuario listar todos los roles ligados al proyecto, ademas, el template relacionado concede 
        las opciones para agregar un rol seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    roles = Rol.objects.all()
    ctx = {'proyecto':proyecto, 'roles':roles}
    return render_to_response('proyecto/agregar_rol.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar rol a proyecto")
@miembro_proyecto()
def proyecto_confirmacion_agregar_rol_view(request, id_proyecto, id_rol):
    """
    ::
    
        La vista de confirmacion de agregacion de un rol a un proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Agregar rol a proyecto.
            - El usuario debe ser miembro del proyecto.
            
        Esta vista permite al usuario agregar un rol seleccionado a un proyecto seleccionado previamente. Se verifica si el rol a agregar ya 
        pertenece al proyecto, en cuyo caso se cancelara la operacion.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            - id_rol: el identificador del rol.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
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
    ::
    
        La vista para quitar un rol de un proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Quitar rol de proyecto.
            - El usuario debe pertenecer al proyecto.
            
        Esta vista permite al usuario quitar un rol seleccionado de un proyecto seleccionado previamente.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador de la proyecto.
            - id_rol: el identificador del rol.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
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
    ::
    
        La vista del listado de miembros del comite de un proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Gestionar comite de proyecto.
            - El usuario debe ser miembro del proyecto.
            
        Esta vista permite al usuario listar y conocer las opciones del comite de un proyecto previamente seleccionado.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    miembros = User.objects.filter(comite_de_cambios_proyecto__id=id_proyecto)
    ctx = {'proyecto':proyecto, 'miembros':miembros}
    return render_to_response('proyecto/comite_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def proyecto_agregar_miembro_view(request, id_proyecto):
    """
    ::
    
        La vista del listado de miembros del comite del proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
    
            - El usuario debe estar logueado.
            
        Esta vista permite al usuario listar todos los miembros del comite del proyecto, ademas, el template relacionado concede 
        las opciones para agregar un nuevo usuario al comite.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    usuarios = User.objects.all()
    ctx = {'proyecto':proyecto, 'usuarios':usuarios}
    return render_to_response('proyecto/agregar_miembro.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Agregar miembro a comite")
@miembro_proyecto()
def proyecto_confirmacion_agregar_miembro_view(request, id_proyecto, id_usuario):
    """
    ::
    
        La vista de confirmacion de agregacion de un usuario al comite de un proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Agregar miembro al comite.
            - El usuario debe ser miembro del proyecto.
            
        Esta vista permite al usuario agregar un usuario seleccionado al comite seleccionado previamente. Se verifica si el usuario a agregar ya 
        pertenece al comite, en cuyo caso se cancelara la operacion.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            - id_usuario: el identificador del usuario.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
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
    ::
    
        La vista para quitar un usuario de la lista de miembros del comite de un proyecto. Para acceder a esta vista se deben cumplir los siguientes
        requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Quitar miembro del comite.
            - El usuario debe pertenecer al proyecto.
            
        Esta vista permite al usuario quitar un usuario seleccionado del comite de un proyecto seleccionado previamente.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador de la proyecto.
            - id_usuario: el identificador del usuario.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
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
    ::
    
        Para acceder a esta vista se deben cumplir los siguientes requisitos:
        
            - El usuario debe estar logueado.
            - El usuario debe poseer el permiso: Iniciar proyecto.
            - El usuario debe ser miembro del proyecto.
            
        Permite arrancar un proyecto si es que se cumplen todas las condiciones mencionadas abajo:
    
            - El proyecto debe estar en estado Inactivo.
            - El proyecto debe poseer un lider.
            - El proyecto debe poseer al menos un miembro en su comite de cambios.
            - El proyecto debe poseer al menos un rol.
        
        La vista recibe los siguientes parametros:
        
            - request: contiene informacion sobre la sesion actual.
            - id_proyecto: el identificador del proyecto.
            
        La vista retorna lo siguiente:
        
            - render_to_response: devuelve el contexto, generado en la vista, al template correspondiente. 
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    inicio_valido = True
    estado_valido = True
    comite_valido = True
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
    if proyecto.roles.count() == 0:
        roles_valido = False
        inicio_valido = False
    
    if inicio_valido:
        proyecto.estado = 1
        proyecto.save()
        ctx = {'proyecto':proyecto, 'inicio_valido':inicio_valido, 'estado_valido':estado_valido, 'lider_valido':lider_valido, 'comite_valido':comite_valido, 'roles_valido':roles_valido}
        return render_to_response('proyecto/iniciar_proyecto.html', ctx, context_instance=RequestContext(request))
    else:
        ctx = {'proyecto':proyecto, 'inicio_valido':inicio_valido, 'estado_valido':estado_valido, 'lider_valido':lider_valido, 'comite_valido':comite_valido, 'roles_valido':roles_valido}
        return render_to_response('proyecto/iniciar_proyecto.html', ctx, context_instance=RequestContext(request))