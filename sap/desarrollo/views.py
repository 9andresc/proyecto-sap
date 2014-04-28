from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from administracion.models import Proyecto
from inicio.decorators import permiso_requerido

@login_required(login_url='/login/')
def desarrollo_view(request):
    
    proyectos = Proyecto.objects.filter(estado=1)
    ctx = {'proyectos': proyectos}
    return render_to_response('desarrollo.html', ctx, context_instance=RequestContext(request))