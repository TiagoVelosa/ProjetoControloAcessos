import datetime
from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models.sql.query import RawQuery
from caixas.models import Edificio, Local, Rel_Gestor_Edificio

def edificios_associados_gestor(request):
    gestor = request.user
    edificios = []
    if gestor.is_supergestor:        
        query_set_edificios = Edificio.objects.all()
        if query_set_edificios is not None:
            for edificio in query_set_edificios:
                edificios.append(edificio)

    else:
        relacoes = Rel_Gestor_Edificio.objects.raw('select * from caixas_rel_gestor_edificio where gestor_id = %s and (data_fim > now() or data_fim is NULL);',[gestor.id])
        if relacoes is not None:
            for relacao in relacoes:
                edificio = Edificio.objects.get(id = relacao.edificio_id)
                edificios.append(edificio)
    
    return edificios

def query_set_locais_ativos_associados_a_gestor(request):
    gestor = request.user
    locais = []
    query_set_locais = Local.objects.all()    
    if gestor.is_supergestor:
        query_set_locais = Local.objects.filter( Q(data_fim__gt = datetime.date.today()) | Q(data_fim = None))
        if query_set_locais is not None:
            print(6)
            for local in query_set_locais:
                locais.append(local)    
    else:
        edifcios = edificios_associados_gestor(request)
        count = 0
        for edificio in edifcios:
            if count == 0:                       
                query_set_locais = Local.objects.filter(edificio_id = edificio.id).filter( Q(data_fim__gt = datetime.date.today()) | Q(data_fim = None))
            else:
                aux =  Local.objects.filter(edificio_id = edificio.id).filter( Q(data_fim__gt = datetime.date.today()) | Q(data_fim = None))     
                query_set_locais = query_set_locais | aux
            count += 1
    
    return(query_set_locais)