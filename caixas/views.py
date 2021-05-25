 
from django.shortcuts import render, redirect
from caixas.forms import EdificioForm,LocalForm,PessoaForm, FormAdicionarGestor, Form_Edf_Gestor
from caixas.models import Edificio, Local, Pessoa, Rel_Gestor_Edificio
from users.models import Gestor

# Create your views here.

def teste_view(request):
    return render(request,'base.html')

def edificio_view(request):
    context = {}
    current_user = request.user
    tem_edificio = Rel_Gestor_Edificio.objects.filter(gestor_id=current_user.id)
    context["edificios"] = tem_edificio
    if('edificio_id' in request.POST):
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
            return redirect('locais')            
        
    else:        
        form = LocalForm()
        
    context['locais_form'] = form
    return render(request, "locais.html",context)


def pessoas_view(request):    
    context = {}
    if request.POST:        
        form = PessoaForm(request.POST)
        context['pessoa_form'] = form
        if form.is_valid():
            print(request.POST)
            pessoa = Pessoa()            
            pessoa.first_name = request.POST['first_name']
            pessoa.descricao = request.POST['descricao']
            pessoa.email = request.POST['email']
            pessoa.last_name = request.POST['last_name']
            pessoa.phone_number = request.POST['phone_number']
            pessoa.save()
            return redirect('pessoas')      
    else:        
        form = PessoaForm()
        
    context['pessoa_form'] = form
    return render(request, "pessoas.html",context)