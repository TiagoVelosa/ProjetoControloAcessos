
from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields, widgets
from django.shortcuts import redirect
from caixas.models import Edificio,Local,Pessoa,Cartao, Pessoa_Cartao, Caixa, Caixa_Local, Rel_Gestor_Edificio
from users.models import Gestor



class FormAdicionarGestor(forms.ModelForm):
    first_name = forms.CharField(max_length=15, label = "Primeiro Nome")
    last_name = forms.CharField(max_length=15, label = "Ultimo Nome")
    email = forms.EmailField(max_length=60,help_text="Obrigatório! Insira um endereço de email válido!")
    password = forms.CharField(widget=forms.PasswordInput)
    is_supergestor = forms.BooleanField(required=False, initial=False, label = "Supergestor")
    
    
    class Meta:
        model= Gestor
        fields = ("email","first_name","last_name", "password")

class EdificioForm(forms.ModelForm):
    nome = forms.CharField(label="Nome", max_length=20)
    descricao = forms.CharField(label="Descricão", max_length=50)

    class Meta:
        model = Edificio
        fields=("nome","descricao")
    


class LocalForm(forms.ModelForm):
    nome = forms.CharField(max_length=20, label = "Nome")
    descricao = forms.CharField(label="Descricão", max_length=50)
    edificio = forms.ModelChoiceField(queryset=Edificio.objects.all(),empty_label="Selecione o Edficicio",initial=0)

    data_inicio = forms.DateInput()
    data_fim = forms.DateInput()
    ativo = forms.BooleanField()

    class Meta:
        model = Local
        fields = ("nome","descricao","edificio","data_inicio","data_fim","ativo")


class PessoaForm(forms.ModelForm):
    first_name = forms.CharField(max_length=15, label = "Primeiro Nome")
    last_name = forms.CharField(max_length=15, label = "Ultimo Nome")
    email = forms.EmailField(max_length=60,help_text="Obrigatório! Insira um endereço de email válido!")
    phone_number = forms.CharField(max_length=15 ,label="Número de telemóvel")
    descricao = forms.CharField(max_length = 50, label = "Descrição")

    class Meta:
        model = Pessoa
        fields = ("first_name","last_name","email","phone_number","descricao")

class CartaoForm(forms.ModelForm):
    codigo_hexa = forms.CharField(max_length=50)
    data_desativacao = forms.DateInput()
    

    class Meta:
        model = Cartao
        fields = ("codigo_hexa","data_desativacao")

class Form_Cartao_Pessoa(forms.ModelForm):
    data_inicio = forms.DateInput()
    data_fim = forms.DateInput()
    cartao = forms.ModelChoiceField(queryset=Cartao.objects.all(),empty_label="Selecione o Cartão",initial=0)
    pessoa = forms.ModelChoiceField(queryset=Pessoa.objects.all(),empty_label="Selecione a Pessoa",initial=0)
    
    class Meta:
        model = Pessoa_Cartao
        fields = ("data_inicio","data_fim","cartao","pessoa")


class Form_Caixa_Local(forms.ModelForm):
    local = forms.ModelChoiceField(queryset=Local.objects.all(),empty_label="Selecione o Cartão",initial=0)
    caixa = forms.ModelChoiceField(queryset=Caixa.objects.all(),empty_label="Selecione o Cartão",initial=0)
    data_inicio = forms.DateInput()
    data_fim = forms.DateInput()

    class Meta:
        model = Caixa_Local
        fields = ("local","caixa","data_inicio","data_fim")

class Form_Caixa(forms.ModelForm):
    ativo = forms.BooleanField()
    ip = forms.CharField(max_length=50)
    mac_adress = forms.CharField(max_length=50)
    token_seguranca = forms.CharField(max_length=50)
    no_uso = forms.BooleanField()
    data_desativacao = forms.DateInput()
    
    local_atual_id  = forms.ModelChoiceField(queryset=Local.objects.all(),empty_label="Selecione o Local",initial=0)

    class Meta:
        model = Caixa
        fields = ("ativo","ip","token_seguranca","no_uso","data_desativacao","local_atual_id")

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
