from caixas.database_queries import *
from django.shortcuts import render
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from caixas.models import Local, Caixa_Local
from caixas.forms import LocalForm

def local_details_view(request,id):
    context = {}
    try:
        local = Local.objects.get(id=id)
    except Local.DoesNotExist:
        context['erro_nao_existe'] = "ERRO - Local não encontrado!"
    caixas_local = Caixa_Local.objects.raw("SELECT * FROM caixas_caixa_local where local_id = %s and (data_fim > now() or data_fim is NULL);",[local.id])
    context["local"] =local
    context["caixas"] = caixas_local
    return render(request,"local_details.html",context)

def editar_local_view(request,id):
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    context = {}
    if Local.objects.filter(id=id):
        local = Local.objects.get(id=id)
    else:
        messages.error(request,"Local não encontrado!")
        return render(request,"erro.html",context)   
    
    if request.POST:        
        form = LocalForm(request.POST,instance=local)
        if form.is_valid():
            form.save(gestor_name,"editar")
            messages.success(request, "Local editado com sucesso! ")
            return HttpResponseRedirect("/locais/adicionar")
    else:
        form = LocalForm(instance=local)
    
    context['form']=form
    context['titulo'] = "Local"
    context['header'] = "Editar Local"
    context['button'] = "Editar Local"
    return render(request,'adicionar_editar.html',context)

def adicionar_local_view(request):
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    if request.POST:        
        form = LocalForm(request,request.POST)
        if form.is_valid():
            form.save(gestor_name,"criar")
            messages.success(request, "Local adicionado com sucesso! ") 
            return HttpResponseRedirect('/locais/adicionar') 
    else:        
        form = LocalForm(request)

    context['form'] = form
    context['titulo'] = "Locais"
    context['header'] = "Adicionar Local"
    context['button'] = "Adicionar Local"
    return render(request, "adicionar_editar.html",context)