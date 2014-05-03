Views
=======

Import::

	from django.shortcuts import render_to_response, redirect
	from django.template import RequestContext
	from django.contrib.auth.models import User
	from django.http.response import HttpResponseRedirect
	from django.contrib.auth.decorators import login_required
	from django.contrib.auth import logout
	from administracion.forms import CrearUsuarioForm, ModificarUsuarioForm, CambiarContrasenhaForm, CrearRolForm, ModificarRolForm, CrearTipoAtributoForm, ModificarTipoAtributoForm, CrearProyectoForm, ModificarProyectoForm, CrearFaseForm, ModificarFaseForm, CrearTipoItemForm, ModificarTipoItemForm
	from administracion.models import Rol, Permiso, TipoAtributo, Proyecto, Fase, TipoItem, ValorAtributo
	from inicio.decorators import permiso_requerido, miembro_proyecto, fase_miembro_proyecto



.. automodule:: administracion.views
    :members:
