 

from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from caixas.forms import EdificioForm, Form_Caixa_Local,LocalForm,PessoaForm, FormAdicionarGestor, Form_Edf_Gestor, CartaoForm, Form_Cartao_Pessoa,Form_Caixa
from caixas.models import Edificio, Local, Pessoa, Registo, Rel_Gestor_Edificio, Cartao,Pessoa_Cartao,Caixa, Caixa_Local
from users.models import Gestor
from django.contrib import messages
import datetime

from .utils import render_to_pdf 


def generate_pdf(request, *args, **kwargs):
    registos = Registo.objects.all()
    context = {
        'today': datetime.date.today(), 
        'amount': 39.99,
        'customer_name': 'Cooper Mann',
        'order_id': 1233434,
        'registos': registos,
    }
    pdf = render_to_pdf('pdf/relatorio.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

def associar_pessoa_cartao_view(request): 
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    if request.POST:
        form = Form_Cartao_Pessoa(request.POST)
        if form.is_valid():
            form.save(gestor_name,"criar")
            messages.success(request, "Cartão associado com sucesso! ") 
            return HttpResponseRedirect('/gestores/associar') 

    else:
        form = Form_Cartao_Pessoa()
    
    context["form_rel"] = form

    return render(request,"associar_gestor_edf.html",context)
    

def lista_pessoas_view(request):
    context = {}
    pessoas = Pessoa.objects.all()
    relacoes = Pessoa_Cartao.objects.raw("SELECT * FROM caixas_pessoa_cartao where data_fim > now() or data_fim is NULL;")
    context["lista_pessoas"] = pessoas
    context["relacoes"] = relacoes
    return render(request,"pessoas_lista.html",context)

def lista_cartoes_view(request):
    context = {}
    cartoes = Cartao.objects.all()
    context["lista_cartao"] = cartoes
    relacoes = Pessoa_Cartao.objects.raw("SELECT * FROM caixas_pessoa_cartao where data_fim > now() or data_fim is NULL;")
    context["relacoes"] = relacoes
    return render(request,"cartoes_lista.html",context)

def ativar_caixa(request,caixa_id):
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    try:
        caixa = Caixa.objects.get(id=caixa_id)
    except Caixa.DoesNotExist:
        messages.ERROR("Caixa não existe!")    
    caixa.ativo = True
    if (caixa.ativo):
        messages.success(request,"Caixa ativada com sucesso!")
        caixa.modificado_por= gestor_name
        caixa.data_modificado = datetime.date.today()
        caixa.save()
        return HttpResponseRedirect('/caixas/inativas')

def sucesso_view(request):
    context = {}
    if(request.GET):
        context["mac"] = request.GET["mac"]
        context["ip"] = request.GET["ip"]
        context["datetime"] = request.GET["datetime"]
        context["rfid"] = request.GET["rfid"]
        context["h"] = request.GET["h"]        

    return render(request,"sucesso.html",context)

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



def local_editar_view(request,id):
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    try:
        local = Local.objects.get(id=id)
    except Local.DoesNotExist:
        context['erro_nao_existe'] = "ERRO - Local não encontrado!"
    form_local = LocalForm(instance=local)
    
    if request.POST:        
        form_local = LocalForm(request.POST,instance=local)
        if form_local.is_valid():           
            form_local.save(gestor_name,"editar")
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

def gestores_lista(request):    
    context = {}   
    gestores = Gestor.objects.all()
    context["gestores"] = gestores
    return render(request,'gestores_lista.html',context )

def adicionar_edf(request): 
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)    
    form_edf = EdificioForm()
    context["form"] = form_edf
    if request.POST:
        form_edf = EdificioForm(request.POST)
        if form_edf.is_valid():            
            form_edf.save(gestor_name,"criar")
            messages.success(request, "Edificio criado com sucesso! ") 
            return HttpResponseRedirect('/edificio/adicionar') 
    return render(request,"adicionar_edf.html",context)

def gestores_editar_view(request,id):
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    try:
        gestor = Gestor.objects.get(id=id)
    except Gestor.DoesNotExist:
        messages.ERROR(request,"Erro gestor não existe")
    form_gestor = FormAdicionarGestor(instance=gestor)
    
    if request.POST:        
        form_gestor = FormAdicionarGestor(request.POST,instance=gestor)
        if form_gestor.is_valid():           
            form_gestor.save()
            messages.success(request, "Gestor editado com sucesso! ") 
            return HttpResponseRedirect('/locais/adicionar') 
    
    
    context['form_gestor']=form_gestor    
    return render(request,"gestores_editar.html",context)

def gestores_adicionar_view(request): 
    context = {}       
    form_gestor = FormAdicionarGestor()    
    if request.POST:        
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
            messages.success(request, "Gestor criado com sucesso! ") 
            return HttpResponseRedirect('/gestores/adicionar')
    
    context['form_gestor'] = form_gestor
    return render(request, "gestores_adicionar.html",context)


def adicionar_caixa_view(request): 
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name) 
    form_caixa = Form_Caixa()
    context['form_caixa'] = form_caixa
    if request.POST:        
        form_caixa = Form_Caixa(request.POST)
        if form_caixa.is_valid():
            form_caixa.save(gestor_name,"criar")
            messages.success(request, "Caixa criada com sucesso! ") 
            return HttpResponseRedirect('/caixas/adicionar')         
    return render(request, "adicionar_caixa.html",context)



def locais_view(request):     
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    if request.POST:        
        form = LocalForm(request.POST)
        if form.is_valid():
            form.save(gestor_name,"criar")
            messages.success(request, "Local adicionado com sucesso! ") 
            return HttpResponseRedirect('/locais/adicionar') 
    else:        
        form = LocalForm()
    context['locais_form'] = form
    return render(request, "locais.html",context)

def gestores_associar_edf_view(request):
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    if request.POST:
        form = Form_Edf_Gestor(request.POST)
        if form.is_valid():
            form.save(gestor_name,"criar")
            messages.success(request, "Gestor associado com sucesso! ") 
            return HttpResponseRedirect('/gestores/associar') 

    else:
        form = Form_Edf_Gestor()
    
    context["form_rel"] = form

    return render(request,"associar_gestor_edf.html",context)

def caixas_associar_local(request):
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    if request.POST:
        form = Form_Caixa_Local(request.POST)
        if form.is_valid():
            form.save(gestor_name,"criar")
            messages.success(request, "Caixa associada com sucesso! ") 
            return HttpResponseRedirect('/caixas/associar') 

    else:
        form = Form_Caixa_Local()
    
    context["form"] = form

    return render(request,"caixas_associar.html",context)

def adicionar_cartao(request): 
    context = {}
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    form_cartao = CartaoForm()
    context['cartao_form'] = form_cartao
    if request.POST:
        form_cartao = CartaoForm(request.POST) 
        if form_cartao.is_valid():            
            form_cartao.save(gestor_name,"criar")
            messages.success(request, "Cartão adicionado com sucesso! ") 
            return HttpResponseRedirect('/cartoes/adicionar')
    

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

def lista_edfs(request):
    context ={}
    edificios = Edificio.objects.all()
    context["edificios"] = edificios
    return render(request,"lista_edfs.html",context)

def cartoes_editar_view(request,id):
    user = request.user
    gestor_name = str(user.first_name + " " + user.last_name)
    context = {}
    try:
        cartao = Cartao.objects.get(id=id)
    except Cartao.DoesNotExist:
        messages.ERROR(request,"Cartão não existe!")
    form = CartaoForm(instance=cartao)
    
    if request.POST:        
        form = CartaoForm(request.POST,instance=cartao)
        context['form_editar_cartao'] = form
        if form.is_valid():           
            form.save(gestor_name,"editar")
            messages.success(request, "Cartão editado com sucesso! ") 
            return HttpResponseRedirect("/cartoes/adicionar")
    
    context['form_editar_cartao']=form
    return render(request,'cartoes_editar.html',context)


def registos_view(request): #isto tá por fazer ñ sei como xd
    context = {}
    query = "select * from caixas_registo"
    edificios = []
    current_user = request.user
    if(current_user.is_supergestor):
        edificios = Edificio.objects.all()
    else:
        relacoes = Rel_Gestor_Edificio.objects.raw('select * from caixas_rel_gestor_edificio where gestor_id = %s and (data_fim > now() or data_fim is NULL);',[current_user.id])
        for rel in relacoes:
            edificios.append(rel.edf)

    context["edificios"] = edificios
    
    if request.GET:
        if "edificio" in request.GET:
            locais = Local.objects.filter(edificio_id = request.GET["edificio"])
            for local in locais:
                prixnt = Registo.objects.filter(local_atual_caixa = local.nome)
        else:
            print("")
    else:
        registos = Registo.objects.raw(query)
        context['registos'] = registos
    
    
    return render(request,'registos.html',context)

