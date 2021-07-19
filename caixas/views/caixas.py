from django.shortcuts import render
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from caixas.models import Caixa , Edificio, Local,Rel_Gestor_Edificio, Caixa_Local
from caixas.forms import Form_Caixa
import datetime

def caixa_details_view(request, id):
    context = {}
    if Caixa.objects.filter(id=id):
        caixa = Caixa.objects.get(id=id)
    else:
        messages.error(request,"Caixa não existe!")
        return render(request,"erro.html",context)
    context["caixa"] = caixa
    relacoes = Caixa_Local.objects.raw('select * from caixas_caixa_local where caixa_id = %s',[id])
    context["relacoes"] = relacoes

    return render(request,"caixa_details.html",context)

def ativar_caixa(request,caixa_id):
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    try:
        caixa = Caixa.objects.get(id=caixa_id)
    except Caixa.DoesNotExist:
        messages.ERROR("Caixa não existe!")    
    caixa.utilizavel = True
    if (caixa.utilizavel):
        messages.success(request,"Caixa ativada com sucesso!")
        caixa.modificado_por= gestor_name
        caixa.data_modificado = datetime.date.today()
        caixa.save()
        return HttpResponseRedirect('/caixas/')

def desativar_caixa(request,caixa_id):
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    try:
        caixa = Caixa.objects.get(id=caixa_id)
    except Caixa.DoesNotExist:
        messages.ERROR("Caixa não existe!")    
    caixa.utilizavel = False
    if (not caixa.utilizavel):
        messages.success(request,"Caixa desativada com sucesso!")
        caixa.modificado_por= gestor_name
        caixa.data_modificado = datetime.date.today()
        caixa.save()
        return HttpResponseRedirect('/caixas/')

def caixas_inativas(request):
    context = {}
    caixas_inativas  = Caixa.objects.filter(utilizavel = False)
    context['caixas_inativas'] = caixas_inativas

    return render(request, "caixas_inativas.html",context)

def editar_caixa_view(request,id):
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    context = {}
    if Caixa.objects.filter(id=id):
        local = Caixa.objects.get(id=id)
    else:
        messages.error(request,"Caixa não encontrada!")
        return render(request,"erro.html",context)   
    
    if request.POST:        
        form = Form_Caixa(request.POST,instance=local)
        if form.is_valid():
            form.save(gestor_name,"editar")
            messages.success(request, "Caixa editada com sucesso! ")
            return HttpResponseRedirect("/caixas/adicionar")
    else:
        form = Form_Caixa(instance=local)
    
    context['form']=form
    context['titulo'] = "Caixa"
    context['header'] = "Editar Caixa"
    context['button'] = "Editar Caixa"
    return render(request,'adicionar_editar.html',context)

def adicionar_caixa_view(request): 
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)    
    if request.POST:
        form_caixa = Form_Caixa(request.POST)
        if form_caixa.is_valid():            
            form_caixa.save(gestor_name,"criar")
            messages.success(request, "Caixa criada com sucesso!") 
            return HttpResponseRedirect('/caixas/adicionar')
    else:
        form_caixa = Form_Caixa(None)

    context['form'] = form_caixa
    context['titulo'] = "Caixa"
    context['header'] = "Adicionar Caixa"
    context['button'] = "Adicionar Caixa"
    return render(request, "adicionar_editar.html",context)


def caixas_view(request):
    context = {}
    caixas = Caixa.objects.all()
    
    context["caixas"] = caixas
    return render(request,'caixas.html',context)


def caixas_view_ids(request, id_local):
    context = {}    
    current_user = request.user
    tem_edificio = Rel_Gestor_Edificio.objects.filter(gestor_id=current_user.id)
    total = tem_edificio.count()
    context["edificios"] = tem_edificio
    context["total"] = total

    local = Local.objects.get(id = id_local)
    edificio = Edificio.objects.get(id = local.edificio_id)
    caixas_local = Caixa_Local.objects.filter(local_id = id_local)
    locais = Local.objects.filter(edificio_id = edificio.id)
    context["local"] = local.nome
    context["caixas_local"] = caixas_local
    context["edificio"] = edificio.nome
    context["locais_edf"] = locais
    if(total ==1):
        edificio = Edificio.objects.get(id = tem_edificio[0].edificio_id)
        local = Local.objects.filter(edificio_id = edificio.id)
        context["locais_edf"] = local
        context["edificio"] = edificio.nome
    elif('edificio_id' in request.POST):
        locais = Local.objects.filter(edificio_id = request.POST['edificio_id'])
        context["locais_edf"] = locais
        context["edificio"] = Edificio.objects.get(id = request.POST['edificio_id']).nome
    elif('local_id' in request.POST):
        edificio = Edificio.objects.get(id =Local.objects.get(id = request.POST['local_id']).edificio_id)
        locais = Local.objects.filter(edificio_id = edificio.id)
        caixas_local = Caixa_Local.objects.filter(local_id = request.POST['local_id'])
        context["caixas_local"] = caixas_local
        context["local"] = Local.objects.get(id = request.POST['local_id']).nome
        context["locais_edf"] = locais
        context["edificio"] = edificio