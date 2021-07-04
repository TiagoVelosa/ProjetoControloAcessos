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
    caixa.ativo = True
    if (caixa.ativo):
        messages.success(request,"Caixa ativada com sucesso!")
        caixa.modificado_por= gestor_name
        caixa.data_modificado = datetime.date.today()
        caixa.save()
        return HttpResponseRedirect('/caixas/inativas')

def caixas_inativas(request):
    context = {}
    caixas_inativas  = Caixa.objects.filter(ativo = 0)
    context['caixas_inativas'] = caixas_inativas

    return render(request, "caixas_inativas.html",context)

def caixas_editar_view(request,id):
    context = {}
    try:
        caixa = Caixa.objects.get(id=id)
    except Caixa.DoesNotExist:
        context['erro_nao_existe'] = "ERRO - Caixa não encontrada!"
    form_caixa = Form_Caixa(instance=caixa)
    
    if request.POST:        
        form_caixa = Form_Caixa(request.POST,instance=caixa)
        context['caixas_form'] = form_caixa
        if form_caixa.is_valid():
           
            form_caixa.save()
            context['sucesso'] = "Caixa editada com sucesso!"
            form_caixa = Form_Caixa()
            return HttpResponseRedirect("cartoes_editar")
    
    
    context['caixas_form']=form_caixa
    return render(request,'caixas_editar.html',context)

def adicionar_caixa_view(request): 
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name) 
    form_caixa = Form_Caixa()
    context['form_caixa'] = form_caixa
    if request.POST:        
        form_caixa = Form_Caixa(request.POST)
        if form_caixa.is_valid():
            form_caixa.save(gestor_name,"criar")
            messages.success(request, "Caixa criada com sucesso! ") 
            return HttpResponseRedirect('/caixas/adicionar')         
    return render(request, "adicionar_caixa.html",context)

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