from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from caixas.forms import Form_Cartao_Pessoa
from django.contrib import messages


def associar_pessoa_cartao_view(request): 
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    if request.POST:
        form = Form_Cartao_Pessoa(request.POST)
        if form.is_valid():
            form.save(gestor_name,"criar")
            messages.success(request, "Cartão associado com sucesso! ") 
            return HttpResponseRedirect('/gestores/associar') 

    else:
        form = Form_Cartao_Pessoa()
    
    context["form_rel"] = form

    return render(request,"associar_cartao_pessoa.html",context)