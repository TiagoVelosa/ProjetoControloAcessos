from django.shortcuts import render
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from caixas.forms import Form_Caixa_Local

def associar_caixa_local_view(request): 
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)    
    if request.POST:
        form = Form_Caixa_Local(request,request.POST)
        if form.is_valid():            
            form.save(gestor_name,"criar")
            messages.success(request, "Caixa associada com sucesso! ") 
            return HttpResponseRedirect('/caixas/associar')
    else:
        form = Form_Caixa_Local(request)

    context['form'] = form
    context['titulo'] = "Caixa"
    context['header'] = "Associar Caixa"
    context['button'] = "Associar Caixa"
    return render(request, "adicionar_editar.html",context)