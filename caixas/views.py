 
from django.shortcuts import render, redirect
from caixas.forms import EdificioForm, Form_Caixa_Local,LocalForm,PessoaForm, FormAdicionarGestor, Form_Edf_Gestor, CartaoForm, Form_Cartao_Pessoa,Form_Caixa
from caixas.models import Edificio, Local, Pessoa, Rel_Gestor_Edificio, Cartao,Pessoa_Cartao,Caixa, Caixa_Local
from users.models import Gestor

# Create your views here.

def teste_view(request):
    return render(request,'base.html')

def edificio_view(request):
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
            context['sucesso'] = "Local editado com sucesso!"
            form_local = LocalForm()
    
    
    context['locais_form']=form_local
    return render(request,'locais_editar.html',context)

def caixas_view(request):
    return render(request,'caixas.html')


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
            return redirect('gestores') 



        
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
    if request.POST:       
        form_gestor = FormAdicionarGestor(request.POST) 
        form_edificio = EdificioForm(request.POST)
        form_edf_gestor= Form_Edf_Gestor(request.POST)
        
        if form_edificio.is_valid():
            edf = Edificio()            
            edf.nome = request.POST['nome']
            edf.descricao = request.POST['descricao']
            edf.save()
            return redirect('gestores')    
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
            return redirect('gestores')
        if form_edf_gestor.is_valid():            
            form_edf_gestor.save()
            return redirect('gestores')
    else:        
        form_edificio = EdificioForm()
        form_gestor = FormAdicionarGestor()
        form_edf_gestor = Form_Edf_Gestor()
        
    context['edificio_form'] = form_edificio
    context['form_rel'] = form_edf_gestor
    context['form_gestor'] = form_gestor
    return render(request, "gestores.html",context)


def adicionar_caixa_view(request):
    context = {}
    form_caixa = Form_Caixa()
    form_caixa_local = Form_Caixa_Local()
    if request.POST:        
        form_caixa = Form_Caixa(request.POST)
        form_caixa_local = Form_Caixa_Local(request.POST)
        if form_caixa.is_valid():
            print(request.POST)  
            form_caixa.save()
            form_caixa = Form_Caixa()
            context['mensagem'] = "Caixa adicionado com sucesso! " 
        if form_caixa_local.is_valid():
            form_caixa_local.save()
            form_caixa_local = Form_Caixa_Local()
            context['mensagem'] = "Relação adicionada com sucesso! "              
        
    else:        
        form_caixa = Form_Caixa()
        form_caixa_local = Form_Caixa_Local()

    context['form_caixa'] = form_caixa
    context['form_caixa_local'] = form_caixa_local
    return render(request, "adicionar_caixa.html",context)

def locais_view(request):    
    context = {}
    if request.POST:        
        form = LocalForm(request.POST)
        context['locais_form'] = form
        if form.is_valid():
            print(request.POST)
            local = Local()            
            local.nome = request.POST['nome']
            local.descricao = request.POST['descricao']
            local.data_fim = request.POST['data_fim']
            local.data_inicio = request.POST['data_inicio']
            local.edificio = Edificio.objects.get(pk=request.POST['edificio'])
            if (request.POST['ativo'] =="on"):
                local.ativo = True
            else:
                local.ativo = False

            local.save()
            form = LocalForm()
            context['mensagem'] = "Local adicionado com sucesso! "

                      
        
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
            return redirect('cartoes')
        if form_cartao_pessoa.is_valid():

            form_cartao_pessoa.save()
            return redirect('cartoes')
        if form_editar_cartao.isvalid():
            cartao = Cartao()  
            relacao = Pessoa_Cartao.objects.get(id=request.POST['form_editar_cartao'])
            form_cartao_pessoa = Form_Cartao_Pessoa(instance=relacao)
            context['form_rel_pessoa_cartao'] = form_cartao_pessoa      
            cartao.ativo = request.POST['ativo']
            cartao.codigo_hexa = request.POST['codigo_hexa']
            cartao.save()
            return redirect('cartoes')
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


def pessoas_view(request):    
    context = {}
    if request.POST:        
        form = PessoaForm(request.POST)
        context['form_pessoa'] = form
        if form.is_valid():
            form.save()
            return redirect('pessoas')      
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
    
    context['form_editar_cartao']=form_cartao_pessoa
    return render(request,'cartoes_editar.html',context)