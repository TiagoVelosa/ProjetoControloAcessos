from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from users.models import Gestor



class FormRegisto(UserCreationForm):
    email = forms.EmailField(max_length=60,help_text="Obrigatório! Insira um endereço de email válido!")
    

    class Meta:
        model = Gestor
        fields = ("email","first_name","last_name", "password1", "password2")

class GestorAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Gestor
        fields = ("email", "password")
    
    def clean(self):
        email = self.cleaned_data["email"]
        try:
            match = Gestor.objects.get(email=email)
        except Gestor.DoesNotExist:
            raise forms.ValidationError("Email não existe")

        
        password = self.cleaned_data["password"]
        if not authenticate(email=email,password = password):
            raise forms.ValidationError("Password incorreta! Tente novamente! ")
