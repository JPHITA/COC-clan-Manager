from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

from .forms import ConstantesForm
from .models import Constantes
from COC_API import COC_API

import os

# Create your views here.

@csrf_protect
def ViewConstantes(request, id_delete=None, msg_error=None):
    
    if request.method == 'POST':
        id = request.POST.get('id_cons')

        if id != "": # update
            cons = Constantes.objects.get(id=id)
            form = ConstantesForm(request.POST, instance=cons)

            if request.POST["nombre"] == "token COC_API": COC_API.token = request.POST["valor"]

        else: # create
            form = ConstantesForm(request.POST)

        if form.is_valid():
            form.save()
    
    elif id_delete != None: # delete
        Constantes.objects.get(id=id_delete).delete()
        return redirect('/Config/Constantes')
    
    elif msg_error != None: # si hay un error
        os.system("start chrome https://developer.clashofclans.com/")
    
    form = ConstantesForm()
    cons = Constantes.objects.all()
    return render(request, 'Constantes.html', {'form': form, 'cons': cons, 'msg_error': msg_error})