from django.template import RequestContext
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from inicio.forms import LoginForm
from django.shortcuts import render_to_response

def login_view(request):
    valido = True
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                usuario = authenticate(username=username, password=password)
                if usuario is not None and usuario.is_active:
                    login(request, usuario)
                    return HttpResponseRedirect('/')
                else:
                    valido = False
        form = LoginForm()
        ctx = {"form":form, "valido":valido}
        return render_to_response("login.html", ctx, context_instance=RequestContext(request))
    
def logout_view(request):
    logout(request)
    return  HttpResponseRedirect('/')