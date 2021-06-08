
from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields, widgets
from django.shortcuts import redirect
from caixas.models import Edificio,Local,Pessoa,Cartao, Pessoa_Cartao, Caixa, Caixa_Local, Rel_Gestor_Edificio
from users.models import Gestor
from caixas.widgets import PickerInput


class FormAdicionarGestor(forms.ModelForm):
    first_name = forms.CharField(max_length=15, label = "Primeiro Nome")
    last_name = forms.CharField(max_length=15, label = "Ultimo Nome")
    email = forms.EmailField(max_length=60,help_text="Obrigatório! Insira um endereço de email válido!")
    password = forms.CharField(widget=forms.PasswordInput)
    is_supergestor = forms.BooleanField(required=False, initial=False, label = "Supergestor")
    
    
    class Meta:
        model= Gestor
        fields = ("email","first_name","last_name", "password")
    
    def clean(self):
        cleaned_data= super(FormAdicionarGestor,self).clean()
        email = cleaned_data["email"]
        if(Gestor.objects.filter(email = email)):
            raise forms.ValidationError("Já existe um gestor com esse email!")

class EdificioForm(forms.ModelForm):
    nome = forms.CharField(label="Nome", max_length=20)
    descricao = forms.CharField(label="Descricão", max_length=50)

    class Meta:
        model = Edificio
        fields=("nome","descricao")
    
    def clean(self):
        cleaned_data = super(EdificioForm,self).clean()
        nome = cleaned_data["nome"]
        if(Edificio.objects.filter(nome = nome)):
            raise forms.ValidationError("Já existe um edifício com esse nome!")
    
class DateInput(forms.DateInput):
    input_type='date'

class LocalForm(forms.ModelForm):
    nome = forms.CharField(max_length=20, label = "Nome",widget=forms.TextInput(attrs={'placeholder': 'Nome do Edificio', 'style': 'width: 50%; height: 30px;'}))
    descricao = forms.CharField(label="Descricão", max_length=50,widget=forms.TextInput(attrs={'placeholder': 'Descrição do Edificio', 'style': 'width: 50%; height: 30px;'}))
    edificio = forms.ModelChoiceField(queryset=Edificio.objects.all(),empty_label="Selecione o Edficicio",widget=forms.Select(attrs={'style': 'width:50%; height:10%;'}))

    data_inicio = forms.DateTimeField(widget=DateInput())
    data_fim = forms.DateTimeField(widget=DateInput())
    

    class Meta:
        model = Local
        fields = ("nome","descricao","edificio","data_inicio","data_fim",)

    def clean(self):
        cleaned_data = super(LocalForm, self).clean()
        if not cleaned_data['data_fim']:
            cleaned_data['data_fim'] = None

        nome = cleaned_data['nome']
        descricao = cleaned_data['descricao']
        data_inicio = cleaned_data['data_inicio']
        data_fim = cleaned_data['data_fim']
        if(Local.objects.filter(data_inicio=data_inicio, nome=nome, descricao = descricao, data_fim=data_fim).exists()):
            raise forms.ValidationError("Esse local já existe! ")
        if(data_fim != None):
            if(data_inicio>data_fim):
                raise forms.ValidationError("A data final não pode ser anterior à inicial")    
        return cleaned_data

class PessoaForm(forms.ModelForm):
    first_name = forms.CharField(max_length=15, label = "Primeiro Nome")
    last_name = forms.CharField(max_length=15, label = "Ultimo Nome")
    email = forms.EmailField(max_length=60,help_text="Obrigatório! Insira um endereço de email válido!")
    phone_number = forms.CharField(max_length=15 ,label="Número de telemóvel")
    descricao = forms.CharField(max_length = 50, label = "Descrição")

    class Meta:
        model = Pessoa
        fields = ("first_name","last_name","email","phone_number","descricao")
    
    def clean(self):
        cleaned_data = super(PessoaForm, self).clean()
        first_name = cleaned_data["first_name"]
        last_name = cleaned_data["last_name"]
        email = cleaned_data["email"]
        phone_number = cleaned_data["phone_number"]

        if(Pessoa.objects.filter(first_name=first_name,last_name=last_name,email=email,phone_number=phone_number)):
            raise forms.ValidationError("Já existe uma pessoa com esses dados!")

class CartaoForm(forms.ModelForm):
    codigo_hexa = forms.CharField(max_length=50)

    class Meta:
        model = Cartao
        fields = ("codigo_hexa",)
    
    def clean(self):
        cleaned_data = super(CartaoForm, self).clean()
        codigo_hexa = cleaned_data["codigo_hexa"]
        if(Cartao.objects.filter(codigo_hexa= codigo_hexa)):
            raise forms.ValidationError("Já existe um cartão com esse código!")

class Form_Cartao_Pessoa(forms.ModelForm):
    data_inicio = forms.DateInput()
    data_fim = forms.DateInput()
    cartao = forms.ModelChoiceField(queryset=Cartao.objects.all(),empty_label="Selecione o Cartão",initial=0)
    pessoa = forms.ModelChoiceField(queryset=Pessoa.objects.all(),empty_label="Selecione a Pessoa",initial=0)
    
    class Meta:
        model = Pessoa_Cartao
        fields = ("data_inicio","data_fim","cartao","pessoa")

    def clean(self):
        cleaned_data = super(Form_Cartao_Pessoa, self).clean()
        if not cleaned_data['data_fim']:
            cleaned_data['data_fim'] = None

        cartao = cleaned_data['cartao']
        pessoa = cleaned_data['pessoa']
        data_inicio = cleaned_data['data_inicio']
        data_fim = cleaned_data['data_fim']
        if(Pessoa_Cartao.objects.filter(data_inicio=data_inicio, cartao=cartao, pessoa = pessoa, data_fim=data_fim).exists()):
            raise forms.ValidationError("Cartão já associado com esses dados!")
        if(data_fim != None):
            if(data_inicio>data_fim):
                raise forms.ValidationError("A data final não pode ser anterior à inicial")    
        return cleaned_data


class Form_Caixa_Local(forms.ModelForm):
    local = forms.ModelChoiceField(queryset=Local.objects.all(),empty_label="Selecione o Cartão",initial=0)
    caixa = forms.ModelChoiceField(queryset=Caixa.objects.all(),empty_label="Selecione o Cartão",initial=0)
    data_inicio = forms.DateInput()
    data_fim = forms.DateInput()

    class Meta:
        model = Caixa_Local
        fields = ("local","caixa","data_inicio","data_fim")
    
    def clean(self):
        cleaned_data = super(Form_Caixa_Local, self).clean()
        if not cleaned_data['data_fim']:
            cleaned_data['data_fim'] = None

        local = cleaned_data['local']
        caixa = cleaned_data['caixa']
        data_inicio = cleaned_data['data_inicio']
        data_fim = cleaned_data['data_fim']
        if(Caixa_Local.objects.filter(data_inicio=data_inicio, local=local, caixa = caixa, data_fim=data_fim).exists()):
            raise forms.ValidationError("Já existe uma caixa adicionada com esses dados!")
        if(data_fim != None):
            if(data_inicio>data_fim):
                raise forms.ValidationError("A data final não pode ser anterior à inicial")    
        return cleaned_data

class Form_Caixa(forms.ModelForm):
    
    ip = forms.CharField(max_length=50)
    mac_adress = forms.CharField(max_length=50)
    token_seguranca = forms.CharField(max_length=50)
    ativo = forms.BooleanField(required=False, initial=False, label = "Ativo")
    class Meta:
        model = Caixa
        fields = ("ip","mac_adress","token_seguranca","ativo")

    def clean(self):
        cleaned_data = super(Form_Caixa, self).clean()
        ip = cleaned_data['ip']
        token_seguranca = cleaned_data['token_seguranca']
        if(Caixa.objects.filter(ip = ip)):
            raise forms.ValidationError("Já existe uma caixa com esse ip!")
        if(Caixa.objects.filter(token_seguranca=token_seguranca)):
            raise forms.ValidationError("Já existe uma caixa com esse token!")
        return cleaned_data

class Form_Edf_Gestor(forms.ModelForm):
    data_inicio = forms.DateInput()
    data_fim = forms.DateInput()
    gestor = forms.ModelChoiceField(queryset=Gestor.objects.all(),empty_label="Selecione o Gestor",initial=0)
    edificio = forms.ModelChoiceField(queryset=Edificio.objects.all(),empty_label="Selecione o Edficicio",initial=0)

    class Meta:
        model = Rel_Gestor_Edificio
        fields = ('data_inicio',"data_fim","gestor","edificio")

    def clean(self):
        cleaned_data = super(Form_Edf_Gestor, self).clean()
        if not cleaned_data['data_fim']:
            cleaned_data['data_fim'] = None

        gestor = cleaned_data['gestor']
        edificio = cleaned_data['edificio']
        data_inicio = cleaned_data['data_inicio']
        data_fim = cleaned_data['data_fim']
        if(Rel_Gestor_Edificio.objects.filter(data_inicio=data_inicio, gestor=gestor, edificio = edificio, data_fim=data_fim).exists()):
            raise forms.ValidationError("Já existe uma relação com esses dados")
        if(data_fim != None):
            if(data_inicio>data_fim):
                raise forms.ValidationError("A data final não pode ser anterior à inicial")    
        return cleaned_data
