from django.shortcuts import render
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from caixas.models import Cartao , Pessoa_Cartao
from caixas.forms import CartaoForm


def cartoes_details_view(request, id):
    context = {}
    if Cartao.objects.filter(id=id):
        cartao = Cartao.objects.get(id=id)
    else:
        messages.error(request,"Cartão não existe!")
        return render(request,"erro.html",context)
    context["cartao"] = cartao
    relacoes = Pessoa_Cartao.objects.raw('select * from caixas_pessoa_cartao where cartao_id = %s',[id])
    context["relacoes"] = relacoes

    return render(request,"cartao_details.html",context)


def lista_cartoes_view(request):
    context = {}
    cartoes = Cartao.objects.all()
    context["lista_cartao"] = cartoes
    relacoes = Pessoa_Cartao.objects.raw("SELECT * FROM caixas_pessoa_cartao where data_fim > now() or data_fim is NULL;")
    context["relacoes"] = relacoes
    return render(request,"cartoes_lista.html",context)

def editar_cartao_view(request,id):
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    context = {}
    if Cartao.objects.filter(id=id):
        cartao = Cartao.objects.get(id=id)
    else:
        messages.error(request,"Cartão não encontrado!")
        return render(request,"erro.html",context)   
    
    if request.POST:        
        form = CartaoForm(request.POST,instance=cartao)
        if form.is_valid():
            form.save(gestor_name,"editar")
            messages.success(request, "Cartão editado com sucesso! ")
            return HttpResponseRedirect("/cartoes/adicionar")
    else:
        form = CartaoForm(instance=cartao)
    
    context['form']=form
    context['titulo'] = "Cartão"
    context['header'] = "Editar Cartão"
    context['button'] = "Editar Cartão"
    return render(request,'adicionar_editar.html',context)

def adicionar_cartao_view(request): 
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)    
    if request.POST:
        form = CartaoForm(request.POST)
        if form.is_valid():            
            form.save(gestor_name,"criar")
            messages.success(request, "Cartão criado com sucesso! ") 
            return HttpResponseRedirect('/cartoes/adicionar')
    else:
        form = CartaoForm(None)

    context['form'] = form
    context['titulo'] = "Cartão"
    context['header'] = "Adicionar Cartão"
    context['button'] = "Adicionar Cartão"
    return render(request, "adicionar_editar.html",context)