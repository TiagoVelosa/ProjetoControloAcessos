import datetime
from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models.sql.query import RawQuery
from caixas.models import Edificio, Local, Rel_Gestor_Edificio

def query_set_edificios_associados_gestor(request):
    gestor = request.user
    if gestor.is_supergestor:        
        query_set_edificios = Edificio.objects.all()    
    else:
        relacoes = relacoes_ativas_edf_gestor(request)        
        if relacoes is not None:
            count = 0
            for relacao in relacoes:
                if count == 0: 
                    query_set_edificios = Edificio.objects.filter(id = relacao.edificio_id)
                else:
                    aux = Edificio.objects.filter(id = relacao.edificio_id)
                    query_set_edificios = query_set_edificios | aux
                count+=1
    
    return query_set_edificios

def relacoes_ativas_edf_gestor(request):
    gestor = request.user
    return Rel_Gestor_Edificio.objects.filter(gestor_id = gestor.id).filter( Q(data_fim__gt = datetime.date.today()) | Q(data_fim = None))

def relacao_gestor_edf(request):
    gestor = request.user
    return Rel_Gestor_Edificio.objects.filter(gestor_id = gestor.id)



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
        edifcios = query_set_edificios_associados_gestor(request)
        count = 0
        for edificio in edifcios:
            if count == 0:                       
                query_set_locais = Local.objects.filter(edificio_id = edificio.id).filter( Q(data_fim__gt = datetime.date.today()) | Q(data_fim = None))
            else:
                aux =  Local.objects.filter(edificio_id = edificio.id).filter( Q(data_fim__gt = datetime.date.today()) | Q(data_fim = None))     
                query_set_locais = query_set_locais | aux
            count += 1
    
    return query_set_locais