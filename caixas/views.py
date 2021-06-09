 

from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from caixas.forms import EdificioForm, Form_Caixa_Local,LocalForm,PessoaForm, FormAdicionarGestor, Form_Edf_Gestor, CartaoForm, Form_Cartao_Pessoa,Form_Caixa
from caixas.models import Edificio, Local, Pessoa, Registo, Rel_Gestor_Edificio, Cartao,Pessoa_Cartao,Caixa, Caixa_Local
from users.models import Gestor
from django.contrib import messages
from django.http import FileResponse


# Create your views here.
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

def local_details_view(request,id):
    context = {}
    try:
        local = Local.objects.get(id=id)
    except Local.DoesNotExist:
        context['erro_nao_existe'] = "ERRO - Local não encontrado!"
    caixas_local = Caixa_Local.objects.raw("SELECT * FROM caixas_caixa_local where local_id = %s and (data_fim > now() or data_fim is NULL);",[local.id])
    context["local"] =local
    context["caixas"] = caixas_local
    return render(request,"local_details.html",context)

def teste_view(request):
    return render(request,'base.html')

def edf_geral_view(request):
    context = {}
    gestores = {}
    current_user = request.user
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


def caixas_inativas(request):
    context = {}
    caixas_inativas  = Caixa.objects.filter(ativo = 0)
    context['caixas_inativas'] = caixas_inativas

    return render(request, "caixas_inativas.html",context)

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
    tem_edificio = Rel_Gestor_Edificio.objects.raw('select * from caixas_rel_gestor_edificio where gestor_id = %s and (data_fim > now() or data_fim is NULL);',[current_user.id])
    total = len(tem_edificio)
    
    if(total ==1):
        return redirect('edf_historico',id=tem_edificio[0].edificio_id)
    else:
        context["edificios"] = tem_edificio
    return render(request,'historico_edf.html',context)

def edificio_view(request):
    #print(request.POST)
    context = {}    
    current_user = request.user
    tem_edificio = Rel_Gestor_Edificio.objects.raw('select * from caixas_rel_gestor_edificio where gestor_id = %s and (data_fim > now() or data_fim is NULL);',[current_user.id])
    total = len(tem_edificio)
    context["edificios"] = tem_edificio
    context["total"] = total
    if(total ==1):
        edificio = Edificio.objects.get(id = tem_edificio[0].edificio_id)
        local = Local.objects.filter(edificio_id = edificio.id)
        context["locais_edf"] = local
        context["edificio"] = edificio.nome
    elif('edificio_id' in request.POST and request.POST['edificio_id'] != 'Selecione o Edificio'):
        locais = Local.objects.filter(edificio_id = request.POST['edificio_id'])
        context["locais_edf"] = locais
        context["edificio"] = Edificio.objects.get(id = request.POST['edificio_id']).nome
    return render(request,'edificios.html',context)

def input_view(request):
    return render(request, 'inputs.html')

def local_editar_view(request,id):
    context = {}
    try:
        local = Local.objects.get(id=id)
    except Local.DoesNotExist:
        context['erro_nao_existe'] = "ERRO - Local não encontrado!"
    form_local = LocalForm(instance=local)
    
    if request.POST:        
        form = LocalForm(request.POST,instance=local)
        context['locais_form'] = form
        if form.is_valid():           
            form.save()
            messages.success(request, "Local editado com sucesso! ") 
            return HttpResponseRedirect('/locais/adicionar') 
    
    
    context['locais_form']=form_local
    return render(request,'locais_editar.html',context)

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

def gestores_editar(request):
    print(request.POST)
    context = {}
    todos_edificios = Edificio.objects.all()
    todos_gestores = Gestor.objects.all()
    todas_relacoes = Rel_Gestor_Edificio.objects.all()
    context = {
        'todos_edificios': todos_edificios,
        'todos_gestores': todos_gestores,
        'todas_relacoes': todas_relacoes
    }
    id_modelo=0
    if request.POST:
        if('selecionar_gestor_editar' in request.POST):
            gestor = Gestor.objects.get(id=request.POST['selecionar_gestor_editar'])
            form_gestor = FormAdicionarGestor(instance=gestor)          
            context['form_gestor'] = form_gestor
            
        elif('selecionar_edf_editar' in request.POST):
            edificio = Edificio.objects.get(id=request.POST['selecionar_edf_editar'])
            form_edificio = EdificioForm(instance=edificio) 
            context['edificio_form'] = form_edificio
            id_modelo = request.POST['selecionar_edf_editar'] 
        elif('selecionar_relacao_editar' in request.POST):
            relacao = Rel_Gestor_Edificio.objects.get(id=request.POST['selecionar_relacao_editar'])
            form_edf_gestor = Form_Edf_Gestor(instance=relacao)
            context['form_rel'] = form_edf_gestor
            id_modelo = request.POST['selecionar_relacao_editar']
        form_gestor = FormAdicionarGestor(request.POST) 
        form_edificio = EdificioForm(request.POST)
        form_edf_gestor= Form_Edf_Gestor(request.POST)
        if form_edificio.is_valid():
            print("Dentro form")
            print(id_modelo)
            edificio = Edificio.objects.get(id_modelo)
            edificio.nome = request.POST['nome']
            edificio.descricao = request.POST['descricao']
            edificio.save()
            return HttpResponseRedirect('gestores') 



        
    return render(request,'gestores_editar.html',context )

def gestores_view(request): 
    print(request.POST)   
    context = {}
    todos_edificios = Edificio.objects.all()
    todos_gestores = Gestor.objects.all()
    context = {
        'todos_edificios': todos_edificios,
        'todos_gestores': todos_gestores
    }
    form_edificio = EdificioForm()
    form_gestor = FormAdicionarGestor()
    form_edf_gestor = Form_Edf_Gestor()
    if 'nome' in request.POST:
        form_edificio = EdificioForm(request.POST)
        if form_edificio.is_valid():
            edf = Edificio()            
            edf.nome = request.POST['nome']
            edf.descricao = request.POST['descricao']
            edf.save()
            return HttpResponseRedirect('gestores')
    elif 'first_name' in request.POST:
        form_gestor = FormAdicionarGestor(request.POST)     
        if form_gestor.is_valid():
            gestor = Gestor()
            gestor.first_name = request.POST['first_name']
            gestor.last_name = request.POST['last_name']
            gestor.set_password(request.POST['password'])
            gestor.email = request.POST['email']
            if('is_supergestor' in request.POST):
                gestor.is_supergestor = True
            else:
                gestor.is_supergestor = False
            gestor.save()
            return HttpResponseRedirect('gestores')
    elif 'data_inicio' in request.POST:
        form_edf_gestor= Form_Edf_Gestor(request.POST)
        if form_edf_gestor.is_valid():            
            form_edf_gestor.save()
            return HttpResponseRedirect('gestores')
    else:        
        form_edificio = EdificioForm()
        form_gestor = FormAdicionarGestor()
        form_edf_gestor = Form_Edf_Gestor()
        
    context['edificio_form'] = form_edificio
    context['form_rel'] = form_edf_gestor
    context['form_gestor'] = form_gestor
    return render(request, "gestores.html",context)


def adicionar_caixa_view(request):
    print(request.POST)
    
    context = {}
    form_caixa = Form_Caixa()
    form_caixa_local = Form_Caixa_Local()
    if 'ip' in request.POST:        
        form_caixa = Form_Caixa(request.POST)
        print(form_caixa.errors) 
        if form_caixa.is_valid():
            print(form_caixa.errors)  
            form_caixa.save()
            form_caixa = Form_Caixa()
            context['mensagem'] = "Caixa adicionada com sucesso!"
            return HttpResponseRedirect("adicionar")
        else:
            context['erro'] = form_caixa.errors
    elif 'local' in request.POST:
        form_caixa_local = Form_Caixa_Local(request.POST)       
        if form_caixa_local.is_valid():
            form_caixa_local.save()
            form_caixa_local = Form_Caixa_Local()
            context['mensagem'] = "Relação adicionada com sucesso! "   
            return HttpResponseRedirect("adicionar")           
        else:
            context['erro'] = form_caixa_local.errors
    else:        
        form_caixa = Form_Caixa()
        form_caixa_local = Form_Caixa_Local()

    context['form_caixa'] = form_caixa
    context['form_caixa_local'] = form_caixa_local
    return render(request, "adicionar_caixa.html",context)


def sucesso_view(request):
    
    return render(request,"sucesso.html")

def locais_view(request):    
    context = {}
    if request.POST:        
        form = LocalForm(request.POST)
        context['locais_form'] = form
        if form.is_valid():
            form.save()
            messages.success(request, "Local adicionado com sucesso! ") 
            return HttpResponseRedirect('/locais/adicionar') 
    else:        
        form = LocalForm()
    context['locais_form'] = form
    return render(request, "locais.html",context)



def cartoes_view(request):
    print(request.POST)   
    context = {}
    todos_cartoes = Cartao.objects.all()
    todos_pessoas = Pessoa.objects.all()
    todas_relacoes = Pessoa_Cartao.objects.all()
    context = {
        'todos_cartoes': todos_cartoes,
        'todos_pessoas': todos_pessoas,
        'todas_relacoes': todas_relacoes
    }
    if request.POST:
        form_cartao = CartaoForm(request.POST) 
        form_cartao_pessoa = Form_Cartao_Pessoa(request.POST)
        form_editar_cartao = CartaoForm(request.POST)
        if form_cartao.is_valid():
            cartao = Cartao()          
            cartao.ativo = request.POST['ativo']
            cartao.codigo_hexa = request.POST['codigo_hexa']
            cartao.save()
            return HttpResponseRedirect('cartoes')
        if form_cartao_pessoa.is_valid():

            form_cartao_pessoa.save()
            return HttpResponseRedirect('cartoes')
        if form_editar_cartao.isvalid():
            cartao = Cartao()  
            relacao = Pessoa_Cartao.objects.get(id=request.POST['form_editar_cartao'])
            form_cartao_pessoa = Form_Cartao_Pessoa(instance=relacao)
            context['form_rel_pessoa_cartao'] = form_cartao_pessoa      
            cartao.ativo = request.POST['ativo']
            cartao.codigo_hexa = request.POST['codigo_hexa']
            cartao.save()
            return HttpResponseRedirect('cartoes')
    else:        
        form_cartao_pessoa = Form_Cartao_Pessoa()
        form_cartao = CartaoForm()
        form_editar_cartao = CartaoForm()
    context['cartao_form'] = form_cartao
    context['form_rel_pessoa_cartao'] = form_cartao_pessoa
    return render(request,"cartoes.html" ,context)

def caixas_view(request):
    context = {}    
    current_user = request.user
    tem_edificio = Rel_Gestor_Edificio.objects.filter(gestor_id=current_user.id)
    total = tem_edificio.count()
    context["edificios"] = tem_edificio
    context["total"] = total
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

    return render(request,'caixas.html',context)

def pessoas_view(request):    
    context = {}
    if request.POST:        
        form = PessoaForm(request.POST)
        context['form_pessoa'] = form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('pessoas')      
    else:        
        form = PessoaForm()
        
    context['form_pessoa'] = form
    return render(request, "pessoas.html",context)

def pessoas_editar_view(request):    
    context = {}
    try:
        pessoa = Pessoa.objects.get(id=id)
    except Pessoa.DoesNotExist:
        context['erro_nao_existe'] = "ERRO - Pessoa não encontrada!"
    form_pessoa = PessoaForm(instance=pessoa)
    
    if request.POST:        
        form = PessoaForm(request.POST,instance=pessoa)
        context['form_editar_pessoa'] = form
        if form.is_valid():
           
            form.save()
            context['sucesso'] = "Pessoa editada com sucesso!"
            form_pessoa = PessoaForm()
            return HttpResponseRedirect("pessoas_editar")
    
    context['form_editar_pessoa']=form_pessoa
    return render(request,'pessoas_editar.html',context)

def cartoes_view(request):
    print(request.POST)   
    context = {}
    todos_cartoes = Cartao.objects.all()
    todos_pessoas = Pessoa.objects.all()
    todas_relacoes = Pessoa_Cartao.objects.all()
    context = {
        'todos_cartoes': todos_cartoes,
        'todos_pessoas': todos_pessoas,
        'todas_relacoes': todas_relacoes
    }
    if request.POST:
        form_cartao = CartaoForm(request.POST) 
        form_cartao_pessoa = Form_Cartao_Pessoa(request.POST)
        if form_cartao.is_valid():
            form_cartao.save()
            return redirect('cartoes')
        if form_cartao_pessoa.is_valid():
            form_cartao_pessoa.save()
            return redirect('cartoes')
    else:        
        form_cartao_pessoa = Form_Cartao_Pessoa()
        form_cartao = CartaoForm()
    context['cartao_form'] = form_cartao
    context['form_rel_pessoa_cartao'] = form_cartao_pessoa
    return render(request,"cartoes.html" ,context)

def cartoes_editar_view(request,id):
    context = {}
    try:
        cartao = Cartao.objects.get(id=id)
    except Cartao.DoesNotExist:
        context['erro_nao_existe'] = "ERRO - Cartão não encontrado!"
    form_cartao_pessoa = Form_Cartao_Pessoa(instance=cartao)
    
    if request.POST:        
        form = Form_Cartao_Pessoa(request.POST,instance=cartao)
        context['form_editar_cartao'] = form
        if form.is_valid():
           
            form.save()
            context['sucesso'] = "Cartão editado com sucesso!"
            form_cartao_pessoa = Form_Cartao_Pessoa()
            return HttpResponseRedirect("cartao_editar")
    
    context['form_editar_cartao']=form_cartao_pessoa
    return render(request,'cartoes_editar.html',context)


def registos_view(request):
    context = {}
    registos = Registo.objects.all()
    context['registos'] = registos

    return render(request,'registos.html',context)

