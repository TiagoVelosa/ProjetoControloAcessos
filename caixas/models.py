from django.db import models
from users.models import Gestor
# Create your models here.

class Pessoa(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField(verbose_name="email", max_length=60,unique= True, error_messages={'unique': "Já existe uma pessoa registada com este email!"})
    phone_number = models.CharField(max_length=15 ,blank=True)
    descricao = models.CharField(max_length = 50, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Edificio(models.Model):
    nome = models.CharField(max_length=20,unique= True,error_messages={'unique':"Já existe um edifício com esse nome!"})
    descricao = models.CharField(max_length=51, blank=True)
    
    def __str__(self):
        return self.nome

class Local(models.Model):
    nome = models.CharField(max_length=20)
    descricao = models.CharField(max_length=50, blank=True)
    edificio = models.ForeignKey(Edificio, on_delete=models.SET_NULL,null=True)
    data_adicionado = models.DateField(auto_now_add=True)
    data_inicio = models.DateField(blank=True, null=True,help_text = "Formato: YYYY-MM-DD")
    data_fim = models.DateField(blank=True, null=True,help_text = "Formato: YYYY-MM-DD")
    def __str__(self):
        return self.nome   

class Caixa(models.Model):
    ativo = models.BooleanField(default = True)
    local_atual_id = models.ForeignKey(Local,blank=True, null=True,on_delete=models.SET_NULL) #Talvez mudar?
    token_seguranca = models.CharField(max_length=50)
    no_uso = models.BooleanField(default = False)
    data_desativacao = models.DateField(blank=True, null=True)
    data_criacao = models.DateField(auto_now_add=True)
    ip = models.CharField(max_length=50,default="0.0.0.0")
    mac_adress = models.CharField(max_length=50,default="0.0.0.0")
        
    def __str__(self):
        return str(self.ip)

class Cartao(models.Model):
    ativo = models.BooleanField(default=True)
    codigo_hexa = models.CharField(max_length=30, unique=True)
    data_criacao = models.DateField(auto_now_add=True)
    data_desativacao = models.DateField(blank=True, null=True)
    def __str__(self):
        return str(self.codigo_hexa)

class Registo(models.Model):
    caixa = models.ForeignKey(Caixa,on_delete=models.SET_NULL,null=True)
    cartao = models.ForeignKey(Cartao,on_delete=models.SET_NULL,null=True)
    data_caixa = models.DateTimeField(blank=True, null=True)
    data_servidor = models.DateTimeField(blank=True, null=True)
    validado = models.BooleanField(default=True)
    codigo_validacao = models.CharField(max_length=50,default="default")
    

class Caixa_Local(models.Model):
    local = models.ForeignKey(Local,on_delete=models.SET_NULL,null=True)
    caixa = models.ForeignKey(Caixa,on_delete=models.SET_NULL,null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)

class Rel_Gestor_Edificio(models.Model):
    gestor = models.ForeignKey(Gestor,on_delete=models.SET_NULL,null=True)
    edificio = models.ForeignKey(Edificio,on_delete=models.SET_NULL,null=True)
    data_inicio = models.DateField(help_text = "Formato: YYYY-MM-DD Exemplo: 2021-12-31")
    data_fim =models.DateField(null=True, blank=True)

class Pessoa_Cartao(models.Model):
    pessoa = models.ForeignKey(Pessoa,on_delete=models.SET_NULL,null=True)
    cartao = models.ForeignKey(Cartao,on_delete=models.SET_NULL,null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)