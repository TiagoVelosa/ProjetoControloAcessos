from django.db import models
from users.models import Gestor
# Create your models here.

class Pessoa(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField(verbose_name="email", max_length=60,unique= True, error_messages={'unique': "Já existe uma pessoa registada com este email!"})
    phone_number = models.CharField(max_length=15 ,blank=True)
    descricao = models.CharField(max_length = 50, blank=True, null=True)

class Edificio(models.Model):
    nome = models.CharField(max_length=20)
    descricao = models.CharField(max_length=50, blank=True)

class Local(models.Model):
    nome = models.CharField(max_length=20)
    descricao = models.CharField(max_length=50, blank=True)
    edificio = models.ForeignKey(Edificio, on_delete=models.SET_NULL,null=True)
    data_inicio= models.DateField(auto_now_add=True)
    data_fim = models.DateField(blank=True, null=True)
    ativo = models.BooleanField(default=True)   

class Caixa(models.Model):
    ativo = models.BooleanField(default = True)
    local_atual_id = models.ForeignKey(Local,blank=True, null=True,on_delete=models.SET_NULL) #Talvez mudar?
    token_seguranca = models.CharField(max_length=30)
    no_uso = models.BooleanField(default = False)
    data_desativacao = models.DateField(blank=True, null=True)
    data_criacao = models.DateField(auto_now_add=True)
    ip = models.CharField(max_length=30)

class Cartao(models.Model):
    ativo = models.BooleanField(default=True)
    no_uso = models.BooleanField(default=False)
    codigo_hexa = models.CharField(max_length=30)
    data_criacao = models.DateField(auto_now_add=True)
    data_desativacao = models.DateField(blank=True, null=True)

class Registo(models.Model):
    caixa = models.ForeignKey(Caixa,on_delete=models.SET_NULL,null=True)
    cartao = models.ForeignKey(Cartao,on_delete=models.SET_NULL,null=True)
    data_registo = models.DateField(auto_now_add=True)
    data_validação = models.DateField(blank=True, null=True)
    validado = models.BooleanField(default=True)

class Caixa_Local(models.Model):
    local = models.ForeignKey(Local,on_delete=models.SET_NULL,null=True)
    caixa = models.ForeignKey(Caixa,on_delete=models.SET_NULL,null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)

class Rel_Gestor_Edificio(models.Model):
    gestor = models.ForeignKey(Gestor,on_delete=models.SET_NULL,null=True)
    edificio = models.ForeignKey(Edificio,on_delete=models.SET_NULL,null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)

class Pessoa_Cartao(models.Model):
    pessoa = models.ForeignKey(Pessoa,on_delete=models.SET_NULL,null=True)
    cartao = models.ForeignKey(Cartao,on_delete=models.SET_NULL,null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)