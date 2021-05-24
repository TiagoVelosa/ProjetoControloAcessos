from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Gestores(BaseUserManager):
    def create_user(self, email,first_name,last_name, password = None):
        if not email:
            raise ValueError("O gestor precisa ter um email!")
        
        user = self.model(
            email = self.normalize_email(email),
            
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,email,password,first_name,last_name):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,            
            first_name = first_name,
            last_name = last_name,
        )
        user.is_superuser = True
        user.is_supergestor = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_supergestor(self,email,first_name,last_name,password=None):
        user = self.create_user(
            email = self.normalize_email(email),            
            first_name = first_name,
            last_name = last_name,
        )
        user.is_supergestor = True
        user.save(using=self._db)
        return user


class Gestor(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60,unique= True, error_messages={'unique': "Já existe um gestor registado com este email!"})
    date_joined = models.DateField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateField(verbose_name="last login", auto_now = True)
    is_supergestor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)

    objects = Gestores()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name"]

    def __str__(self):
        return self.first_name + " " + self.last_name

    def has_perm(self,perm,obj=None):
        return self.is_supergestor
    
    def has_module_perms(self,app_label):
        return True