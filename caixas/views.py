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
    return render(request,'edificios.html',context)

def input_view(request):
    return render(request, 'inputs.html')

def caixas_view(request):
    return render(request,'caixas.html')


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
        context['edificio_form'] = form_edificio
        context['form_gestor'] = form_gestor
        context['form_rel'] = form_edf_gestor
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
       # if ('data_inicio' in request.POST and 'Gestor_ID' in request.POST and 'Edificio_Id' in request.POST):            
        #    relacao = Rel_Gestor_Edificio()
         #   relacao.edificio = Edificio.objects.get(pk = request.POST.get('Edificio_Id')) 
          #  relacao.gestor = Gestor.objects.get(pk = request.POST.get('Gestor_ID'))
           # relacao.data_inicio = request.POST['data_inicio']
            #if('data_fim' != ""):
             #   relacao.data_fim= request.POST['data_fim']                     
            
            #relacao.save()
            #return redirect('gestores')
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