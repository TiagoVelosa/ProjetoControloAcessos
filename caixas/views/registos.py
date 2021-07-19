from caixas.database_queries import local_caixa_ativa_por_caixa
from django.shortcuts import render
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from caixas.models import Edificio, Local, Pessoa_Cartao, Registo, Rel_Gestor_Edificio,Caixa,Cartao
from ..utils import render_to_pdf 
import datetime
from datetime import datetime

def valida_registo(request):
    reg = Registo()
    if(request.GET):
        if("mac" and "ip" and "datetime" and "rfid" and "h" in request.GET):
            caixa = Caixa.objects.filter(mac_address=request.GET["mac"])
            if(caixa):
                caixa = caixa[0]
                data = datetime.strptime(request.GET["datetime"],"%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H%M%S")
                hash_servidor = request.GET["mac"] + request.GET["ip"] + data + request.GET["rfid"] + caixa.token_seguranca
                print("HASH \!/ \n")
                print(hash_servidor)                
                if ("hash_servidor" == request.GET["h"]): 
                    reg.codigo_hexa_cartao = request.GET["rfid"]
                    reg.data_caixa = request.GET["datetime"]
                    reg.data_servidor = datetime.now()
                    reg.validado = True
                    reg.codigo_validacao = request.GET["h"]
                    reg.criado_por = "Caixa"
                    reg.caixa_id = caixa.id
                    reg.local_atual_caixa = local_caixa_ativa_por_caixa(caixa.id)
                    reg.save()
                    return HttpResponse(status = 200)
                else:
                    reg.codigo_hexa_cartao = request.GET["rfid"]
                    reg.data_caixa = request.GET["datetime"]
                    reg.data_servidor = datetime.now()
                    reg.validado = False
                    reg.codigo_validacao = request.GET["h"]
                    reg.criado_por = "ERRO"
                    reg.caixa_id = caixa.id                    
                    reg.local_atual_caixa = local_caixa_ativa_por_caixa(caixa.id)
                    reg.save()
                    return HttpResponse(status=400) 
            else:
                reg.codigo_hexa_cartao = request.GET["rfid"]
                reg.data_caixa = request.GET["datetime"]
                reg.data_servidor = datetime.now()
                reg.validado = False
                reg.codigo_validacao = request.GET["h"]
                reg.criado_por = "ERRO"
                reg.caixa_id = None
                reg.local_atual_caixa = "Caixa não encontrada"
                reg.save()
                return HttpResponse(status=400)
        else:
            return HttpResponse(status=400)            

    return HttpResponse(status=404)

def dados_caixass_view(request):
    context = {}
    if(request.GET):
        reg = Registo()
        
        caixa = Caixa.objects.filter(mac_address=request.GET["mac"])
        data_caixa = request.GET["datetime"]
        data_servidor = datetime.datetime.now()
            
        
        if(caixa):
            
            caixa = caixa[0]
            local = local_caixa_ativa_por_caixa(caixa.id)
            print(local)
            if(local):
                reg.local_atual_caixa = local.nome
                reg.caixa = caixa  
                reg.codigo_hexa_cartao = request.GET["rfid"]
                reg.codigo_validacao = request.GET["h"]
                reg.data_caixa = data_caixa
                reg.data_servidor = data_servidor
                reg.criado_por = "Caixa"
                if(request.GET["h"] == caixa.token_seguranca):
                    reg.validado = True
                    reg.save()
                    return HttpResponse(status=200)
                else:
                    reg.validado = False
                    reg.save()
                    return HttpResponse(status=400)
                
            else:
                reg.local_atual_caixa = "Caixa não associada"
                reg.caixa = caixa  
                reg.codigo_hexa_cartao = request.GET["rfid"]
                reg.codigo_validacao = request.GET["h"]
                reg.data_caixa = data_caixa
                reg.data_servidor = data_servidor
                reg.criado_por = "Caixa"
                reg.validado= False
                reg.save()
                return HttpResponse(status=400)
            
        else:
            reg.caixa = None
            reg.local_atual_caixa = "Caixa não encontrada!"
            reg.validado = False
            reg.codigo_hexa_cartao = request.GET["rfid"]
            reg.codigo_validacao = request.GET["h"]        
            reg.data_caixa = data_caixa
            reg.data_servidor = data_servidor
            reg.criado_por = "ERRO"
            reg.save()
            return HttpResponse(status=400)

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