from caixas.models import Rel_Gestor_Edificio
from django.shortcuts import render
from caixas.forms import Form_Edf_Gestor
from django.contrib import messages
from django.http.response import HttpResponseRedirect


def historico_rel_edf_gestores(request):
    context = {}
    relacoes = Rel_Gestor_Edificio.objects.all().order_by()
    context["relacoes"] = relacoes

    return render(request,"rel_edf_gestor/historico_rel_edf_gestores.html",context)

def gestores_associar_edf_view(request):
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    if request.POST:
        form = Form_Edf_Gestor(request.POST)
        if form.is_valid():
            form.save(gestor_name,"criar")
            messages.success(request, "Gestor associado com sucesso! ") 
            return HttpResponseRedirect('/gestores/associar') 

    else:
        form = Form_Edf_Gestor()
    
    context["form_rel"] = form

    return render(request,"rel_edf_gestor/associar_gestor_edf.html",context)