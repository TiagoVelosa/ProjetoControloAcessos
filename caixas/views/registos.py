from django.shortcuts import render
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from caixas.models import Edificio, Local, Pessoa_Cartao, Registo, Rel_Gestor_Edificio,Caixa,Cartao
from ..utils import render_to_pdf 
import datetime


def dados_caixas_view(request):
    context = {}
    if(request.GET):
        reg = Registo()
        
        caixa = Caixa.objects.filter(mac_adress=request.GET["mac"], ip = request.GET["ip"])[0]
        data_caixa = request.GET["datetime"]
        data_servidor = datetime.datetime.now()
        local = caixa.local_atual_id
        
        if(caixa):
            reg.caixa = caixa        
        reg.codigo_hexa_cartao = request.GET["rfid"]
        reg.codigo_validacao = request.GET["h"]
        reg.data_caixa = data_caixa
        reg.data_servidor = data_servidor
        reg.criado_por = "Caixa"
        reg.local_atual_caixa = local.nome
        if(request.GET["h"] == caixa.token_seguranca):
            reg.validado = True
        else:
            reg.validado = False
        
        reg.save()
        context["sucesso"] = "Inserido"      
        context["mac"] = request.GET["mac"]
        context["ip"] = request.GET["ip"]
        context["datetime"] = request.GET["datetime"]
        context["rfid"] = request.GET["rfid"]
        context["h"] = request.GET["h"]        
    context["sucesso"] = "ERRO" 

    return HttpResponse(status=404)

def registos_view(request):
    context = {}
    edificios = []
    registos = Registo.objects.all()
    current_user = request.user
    if(current_user.is_supergestor):
        edificios = Edificio.objects.all()
        context["edificios"] = edificios
    else:
        relacoes = Rel_Gestor_Edificio.objects.raw('select * from caixas_rel_gestor_edificio where gestor_id = %s and (data_fim > now() or data_fim is NULL);',[current_user.id])
        for rel in relacoes:
            edificios.append(rel.edificio)
        context["edificios"] = edificios

    for edf in edificios:
        locais = Local.objects.filter(edificio_id = edf.id)
        for local in locais:
            if(registos.filter(local_atual_caixa = local.nome)):
                registos = registos.filter(local_atual_caixa = local.nome)

    if request.GET:
        if "edificio" in request.GET:
            locais = Local.objects.filter(edificio_id = request.GET["edificio"])
            for local in locais:
                if(registos.filter(local_atual_caixa = local.nome)):
                    registos = registos.filter(local_atual_caixa = local.nome)
        if request.GET["data_inicio"] != "":
            registos = registos.filter(data_caixa__gte =  request.GET["data_inicio"])

        if request.GET["data_fim"] != "":        
            registos = registos.filter(data_caixa__lte =  request.GET["data_fim"])

        if "PDF" in request.GET:            
            registos_ordenados = registos.order_by('data_caixa')
            context = {
            'today': datetime.date.today(), 
            'num_registos': registos.count(),
            'first_date': registos_ordenados[0].data_servidor,
            'last_date': registos_ordenados.reverse()[0].data_servidor,
            'registos': registos
            }
            pdf = render_to_pdf('pdf/relatorio.html', context)
            return HttpResponse(pdf, content_type='application/pdf')

    context['registos'] = registos
    return render(request,'registos.html',context)