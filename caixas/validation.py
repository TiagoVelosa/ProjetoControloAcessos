from django.core.exceptions import ValidationError
from caixas.models import Caixa_Local, Cartao, Local, Pessoa,Pessoa_Cartao,Caixa
import datetime
from django import forms
import pytz
from ipaddress import IPv4Address, IPv6Address, ip_address

_DATA_COMECO = datetime.datetime(2021,7,1)
utc = pytz.UTC
DATA_COMECO = _DATA_COMECO.replace(tzinfo=utc)


def verifica_data(data_inicio,data_fim): 
    if(data_inicio < DATA_COMECO):
        raise forms.ValidationError("ERRO: Data inicial anterior a 01/07/2021!")
    if(data_fim != None):
            if(data_inicio>data_fim):
                raise forms.ValidationError("ERRO: Data inicial maior que a data final!")    
    return

def verifica_mac_address(mac_address):    
    try:
        ip_address(mac_address)
        return       
    except:
        raise forms.ValidationError("ERRO: MAC Address no formato incorreto!")

def verifica_nome(nome):
    if nome.isalpha():
        return
    else:
        raise forms.ValidationError('ERRO: %s possui caracteres inválidos!' % nome)
    
def verifica_numero_telemovel(numero):
    if numero.isdecimal():
        if(len(numero) != 9):
            raise forms.ValidationError("ERRO: Número de telemóvel precisa ter 9 números!")
        else:
            print(numero[0])
            if numero[0] != "9":                
                raise forms.ValidationError("ERRO: Número de telemóvel precisa começar com um 9!")
            else:
                return
    else:
        raise forms.ValidationError("ERRO: Número de telemóvel possui caracteres inválidos!")
    
def verifica_hexadecimal(codigo):
    if(len(codigo) != 16):
            raise forms.ValidationError("ERRO: O código precisa conter 16 caracteres!")
    for char in codigo:
        if ((char < '0' or char > '9') and (char < 'A' or char > 'F') and (char < 'a' or char > 'f')):
            raise forms.ValidationError("Erro: O código precisa ser um número hexadecimal")
    return

def verifica_cartao_no_uso(id,data_inicio,data_fim):
    if Cartao.objects.filter(id=id):
        cartao = Cartao.objects.get(id=id)
    else:
        raise forms.ValidationError("ERRO: O cartão selecionado não foi encontrado!")
    
    bool1 =Pessoa_Cartao.objects.filter(data_inicio__lt = data_inicio, data_fim__gt = data_inicio, cartao_id = id)
    bool2 =Pessoa_Cartao.objects.filter(data_inicio__lt = data_fim, data_fim__gt = data_fim, cartao_id = id)
    if(bool1 or bool2):
        raise forms.ValidationError("ERRO: O cartão já está associado nesse intervalo de tempo!")
    else:
        return

def verifica_pessoa_tem_cartao(id,data_inicio,data_fim):
    if Pessoa.objects.filter(id=id):
        pessoa = Cartao.objects.get(id=id)
    else:
        raise forms.ValidationError("ERRO: A pessoa selecionada não foi encontrada!")
    
    bool1 =Pessoa_Cartao.objects.filter(data_inicio__lt = data_inicio, data_fim__gt = data_inicio, pessoa_id = id)
    bool2 =Pessoa_Cartao.objects.filter(data_inicio__lt = data_fim, data_fim__gt = data_fim, pessoa_id = id)
    if(bool1 or bool2):
        raise forms.ValidationError("ERRO: A pessoa já tem um cartão associado nesse intervalo de tempo!")
    else:
        return  

def verifica_caixa_no_uso(id,data_inicio,data_fim):
    if Caixa.objects.filter(id=id):
        caixa = Caixa.objects.get(id=id)
    else:
        raise forms.ValidationError("ERRO: A caixa selecionada não foi encontrada!")
    
    bool1 =Caixa_Local.objects.filter(data_inicio__lte = data_inicio, data_fim__gte = data_inicio, caixa_id = id)
    bool2 =Caixa_Local.objects.filter(data_inicio__lte = data_fim, data_fim__gte = data_fim, caixa_id = id)
    if(bool1 or bool2):
        raise forms.ValidationError("ERRO: A caixa já está associada a um local nesse intervalo de tempo!")
    else:
        return

def verifica_data_caixa_local(local_id,data_inicio_caixa,data_fim_caixa):
    if Local.objects.filter(id = local_id):
        local = Local.objects.get(id=local_id)
    else:
        raise forms.ValidationError("ERRO: O local selecionado não foi encontrado!")
    
    if(local.data_fim):
        bool_data_inicio = (data_inicio_caixa.date() >= local.data_inicio and data_inicio_caixa.date() <= local.data_fim)
        bool_data_fim = (data_fim_caixa.date() >= local.data_inicio and data_fim_caixa.date() <= local.data_fim)
    else:
        bool_data_inicio = (data_inicio_caixa.date() >= local.data_inicio)
        bool_data_fim = (data_fim_caixa.date() >= local.data_inicio)
    if(bool_data_inicio and bool_data_fim):
        return
    else:
        raise forms.ValidationError("ERRO: A caixa só pode ser associado dentro do intervalo de tempo do local!")
    