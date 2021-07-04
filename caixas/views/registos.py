from django.shortcuts import render
from django.http.response import HttpResponse
from caixas.models import Edificio, Local, Registo, Rel_Gestor_Edificio
from ..utils import render_to_pdf 
import datetime


def dados_caixas_view(request):
    context = {}
    if(request.GET):
        context["mac"] = request.GET["mac"]
        context["ip"] = request.GET["ip"]
        context["datetime"] = request.GET["datetime"]
        context["rfid"] = request.GET["rfid"]
        context["h"] = request.GET["h"]        

    return render(request,"sucesso.html",context)

def registos_view(request):
    context = {}
    edificios = []
    registos = Registo.objects.all()
    reg = []
    current_user = request.user
    if(current_user.is_supergestor):
        edificios = Edificio.objects.all()
        context["edificios"] = edificios
    else:
        relacoes = Rel_Gestor_Edificio.objects.raw('select * from caixas_rel_gestor_edificio where gestor_id = %s and (data_fim > now() or data_fim is NULL);',[current_user.id])
        for rel in relacoes:
            edificios.append(rel.edificio)

        context["edificios"] = edificios
        
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

        if request.GET["PDF"] == "1":
            
            print(registos)
            context = {
            'today': datetime.date.today(), 
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
            'registos': registos,
            }
            pdf = render_to_pdf('pdf/relatorio.html', context)
            return HttpResponse(pdf, content_type='application/pdf')

    for regs in registos:
        reg.append(regs)

    

    context['registos'] = reg
    return render(request,'registos.html',context)