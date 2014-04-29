from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from administracion.models import Proyecto, Fase
from desarrollo.models import Item
from desarrollo.forms import CrearItemForm
from inicio.decorators import permiso_requerido

@login_required(login_url='/login/')
def desarrollo_view(request):
    
    proyectos = Proyecto.objects.filter(estado=1)
    ctx = {'proyectos': proyectos}
    return render_to_response('desarrollo.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar fases de proyecto")
def fases_proyecto_view(request, id_proyecto):
    
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fases = proyecto.fases.all()
    ctx = {'proyecto':proyecto, 'fases':fases}
    return render_to_response('fases_proyecto.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Gestionar items de fase")
def items_fase_view(request, id_fase, id_proyecto):
    
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fase = Fase.objects.get(id=id_fase)
    items = fase.items.all()
    ctx = {'proyecto':proyecto, 'fase':fase, 'items':items}
    return render_to_response('items_fase.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permiso_requerido(permiso="Crear item")
def crear_item_view(request, id_fase, id_proyecto):
    
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
            
            item = Item.objects.create(nombre=nombre, descripcion=descripcion, complejidad=complejidad, costo=costo)
            item.save()
            fase.items.add(item)
            fase.save()
            return HttpResponseRedirect('/desarrollo/items/fase/%s/proyecto/%s/'%(fase.id, proyecto.id))
            
        else:
            ctx = {'form':form, 'fase':fase, 'proyecto':proyecto}
            return render_to_response('crear_item.html', ctx, context_instance=RequestContext(request))
    ctx = {'form':form, 'fase':fase, 'proyecto':proyecto}
    return render_to_response('crear_item.html', ctx, context_instance=RequestContext(request))