Views
=======

Import::

	from django.shortcuts import render_to_response
	from django.http.response import HttpResponseRedirect
	from django.template import RequestContext
	from django.contrib.auth.decorators import login_required
	from administracion.models import Proyecto, Fase, TipoItem, ValorAtributo
	from desarrollo.models import Item
	from desarrollo.forms import CrearItemForm, ModificarItemForm
	from inicio.decorators import permiso_requerido, miembro_proyecto, fase_miembro_proyecto, item_miembro_proyecto




.. automodule:: desarrollo.views
    :members:
