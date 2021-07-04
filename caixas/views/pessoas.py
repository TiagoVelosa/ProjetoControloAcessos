from django.shortcuts import render
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from caixas.models import Pessoa , Pessoa_Cartao
from caixas.forms import PessoaForm

def pessoa_details_view(request, id):
    context = {}
    if Pessoa.objects.filter(id=id):
        pessoa = Pessoa.objects.get(id=id)
    else:
        messages.error(request,"Pessoa não existe!")
        return render(request,"erro.html",context)
    context["pessoa"] = pessoa
    relacoes = Pessoa_Cartao.objects.raw('select * from caixas_pessoa_cartao where pessoa_id = %s',[id])
    context["relacoes"] = relacoes

    return render(request,"pessoa_details.html",context)


def pessoas_view(request): 
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)      
    context = {}
    if request.POST:        
        form = PessoaForm(request.POST)
        context['form_pessoa'] = form
        if form.is_valid():
            form.save(gestor_name,"criar")
            messages.success(request, "Pessoa adicionada com sucesso! ") 
            return HttpResponseRedirect('/pessoas/adicionar')       
    else:        
        form = PessoaForm()
        
    context['form_pessoa'] = form
    return render(request, "pessoas.html",context)

def pessoas_editar_view(request,id):    
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    context = {}
    try:
        pessoa = Pessoa.objects.get(id=id)
    except Pessoa.DoesNotExist:
        messages.ERROR(request,"Pessoa não existe!")
    form_pessoa = PessoaForm(instance=pessoa)
    
    if request.POST:        
        form_pessoa = PessoaForm(request.POST,instance=pessoa)
        if form_pessoa.is_valid():           
            form_pessoa.save(gestor_name,"editar")
            messages.success(request, "Pessoa editada com sucesso! ")  
            return HttpResponseRedirect("/pessoas/adicionar")
    
    context['form_editar_pessoa']=form_pessoa
    
    return render(request,'pessoas_editar.html',context)

def lista_pessoas_view(request):
    context = {}
    pessoas = Pessoa.objects.all()
    relacoes = Pessoa_Cartao.objects.raw("SELECT * FROM caixas_pessoa_cartao where data_fim > now() or data_fim is NULL;")
    context["lista_pessoas"] = pessoas
    context["relacoes"] = relacoes
    return render(request,"pessoas_lista.html",context)