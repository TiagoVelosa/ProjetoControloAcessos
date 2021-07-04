from django.shortcuts import render
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from caixas.models import Local, Edificio,Rel_Gestor_Edificio
from caixas.forms import EdificioForm

def edificio_details_view(request,id):
    context = {}
    gestores = []
    try:
        edf = Edificio.objects.get(id=id)
    except Edificio.DoesNotExist:
        context['erro_nao_existe'] = "ERRO - Edificio não encontrado!"
    
    locais_ativos = Local.objects.raw('select * from caixas_local where edificio_id= %s and (data_fim > now() or data_fim is NULL);', [id])
    gestores_edf = Rel_Gestor_Edificio.objects.raw('select distinct * from caixas_rel_gestor_edificio where edificio_id =%s and (data_fim > now() or data_fim is NULL);', [id])
    for gestor in gestores_edf:
        
        gestores.append(gestor) 
    
    
    context["gestores"] = gestores_edf
    context["edificio"] = edf
    context["locais"] = locais_ativos
    return render(request, 'edificio_details.html',context)

def edf_lista_view(request):
    context = {}
    relacoes = {}
    edificios = Edificio.objects.all()    
    for edf in edificios:
        rel = Rel_Gestor_Edificio.objects.raw('select * from caixas_rel_gestor_edificio where edificio_id = %s and (data_fim >= (now()- interval 1 day)  or data_fim is NULL);',[edf.id])
        relacoes[edf.nome] = rel
    context["lista_edfs"] = edificios
    context["relacoes"] = relacoes
    return render(request, "lista_edf.html", context)

def edf_geral_view(request):
    context = {}
    gestores = {}
    relacoes = {}
    current_user = request.user
    if(current_user.is_supergestor):
        edificios = Edificio.objects.all()    
        for edf in edificios:
            rel = Rel_Gestor_Edificio.objects.raw('select * from caixas_rel_gestor_edificio where edificio_id = %s and (data_fim >= (now()- interval 1 day)  or data_fim is NULL);',[edf.id])
            if(rel):
                relacoes[edf.nome] = rel
        context["lista_edfs"] = edificios
        context["relacoes"] = relacoes
    else:    
        relacoes = Rel_Gestor_Edificio.objects.raw('select * from caixas_rel_gestor_edificio where gestor_id = %s and (data_fim > now() or data_fim is NULL);',[current_user.id])
        for rel in relacoes:
            gestores_edf = Rel_Gestor_Edificio.objects.raw('select distinct * from caixas_rel_gestor_edificio where edificio_id =%s and (data_fim > now() or data_fim is NULL);', [rel.edificio_id])
            edificio = Edificio.objects.get(id = rel.edificio_id)
            nome_gestores = []
            for gestor in gestores_edf:
                nome_gestores.append(gestor.gestor)
            gestores[edificio.nome] = nome_gestores

    context["gestores"] = gestores    
    context["edificios"] = relacoes
    print(context)
    return render(request, 'edificios_geral.html', context)

def historico_edf_id_view(request,id):
    context={}
    try:
        edf = Edificio.objects.get(id=id)
    except Edificio.DoesNotExist:
        context['erro_nao_existe'] = "ERRO - Edf não encontrado!"

    locais = Local.objects.raw("SELECT * FROM caixas_local where edificio_id = %s",[edf.id])
    context["edificio"] = edf
    context["locais"] = locais
    return render(request,"edf_historico.html",context)


def historico_edf_view(request):
    context = {}
    current_user = request.user
    if(current_user.is_supergestor):
        edificios = Edificio.objects.all()
        context["edificios"] = edificios
    else:    
        relacoes = Rel_Gestor_Edificio.objects.raw('select * from caixas_rel_gestor_edificio where gestor_id = %s and (data_fim > now() or data_fim is NULL);',[current_user.id])
        context["edificios"] = relacoes

    print(context)
    return render(request, 'historico_edf.html', context)

def adicionar_edf(request): 
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)    
    form_edf = EdificioForm()
    context["form"] = form_edf
    if request.POST:
        form_edf = EdificioForm(request.POST)
        if form_edf.is_valid():            
            form_edf.save(gestor_name,"criar")
            messages.success(request, "Edificio criado com sucesso! ") 
            return HttpResponseRedirect('/edificio/adicionar') 
    return render(request,"adicionar_edf.html",context)

def editar_edf(request, id): 
    context = {}
    try:
        edf = Edificio.objects.get(id=id)
    except Edificio.DoesNotExist:
        context['erro_nao_existe'] = "ERRO - Edf não encontrado!"
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)    
    form_edf = EdificioForm(instance=edf)
    context["form"] = form_edf
    if request.POST:
        form_edf = EdificioForm(request.POST, instance=edf)
        if form_edf.is_valid():            
            form_edf.save(gestor_name,"editar")
            messages.success(request, "Edificio editado com sucesso! ") 
            return HttpResponseRedirect('/edificio/adicionar') 
    return render(request,"editar_edf.html",context)