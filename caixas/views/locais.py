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

def local_editar_view(request,id):
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    try:
        local = Local.objects.get(id=id)
    except Local.DoesNotExist:
        context['erro_nao_existe'] = "ERRO - Local não encontrado!"
    form_local = LocalForm(instance=local)
    
    if request.POST:        
        form_local = LocalForm(request.POST,instance=local)
        if form_local.is_valid():           
            form_local.save(gestor_name,"editar")
            messages.success(request, "Local editado com sucesso! ") 
            return HttpResponseRedirect('/locais/adicionar') 
    
    
    context['locais_form']=form_local
    return render(request,'locais_editar.html',context)


def locais_view(request):     
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    if request.POST:        
        form = LocalForm(request.POST)
        if form.is_valid():
            form.save(gestor_name,"criar")
            messages.success(request, "Local adicionado com sucesso! ") 
            return HttpResponseRedirect('/locais/adicionar') 
    else:        
        form = LocalForm()
    context['locais_form'] = form
    return render(request, "locais.html",context)