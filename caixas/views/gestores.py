from django.shortcuts import render
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from caixas.models import Gestor, Rel_Gestor_Edificio
from caixas.forms import FormAdicionarGestor, FormEditarGestor

#Completo

def gestores_details_view(request, id):
    context = {}
    if Gestor.objects.filter(id=id):
        gestor = Gestor.objects.get(id=id)
    else:
        messages.error(request,"Gestor não existe!")
        return render(request,"erro.html",context)
    context["gestor"] = gestor
    relacoes = Rel_Gestor_Edificio.objects.raw('select * from caixas_rel_gestor_edificio where gestor_id = %s and (data_fim >= (now()- interval 1 day)  or data_fim is NULL);',[id])
    context["relacoes"] = relacoes

    return render(request,"gestores_details.html",context)


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

def gestores_lista(request):    
    context = {}   
    gestores = Gestor.objects.all()
    context["gestores"] = gestores
    return render(request,'gestores_lista.html',context )

def gestores_editar_view(request,id):
    context = {}
    user = request.user    
    try:
        gestor = Gestor.objects.get(id=id)
    except Gestor.DoesNotExist:
        messages.ERROR(request,"Erro gestor não existe")
    form_gestor = FormEditarGestor(instance=gestor)
    
    if request.POST:        
        form_gestor = FormEditarGestor(request.POST,instance=gestor)
        if form_gestor.is_valid():           
            form_gestor.save()
            messages.success(request, "Gestor editado com sucesso! ") 
            return HttpResponseRedirect('/locais/adicionar') 
    
    
    context['form_gestor']=form_gestor    
    return render(request,"gestores_editar.html",context)