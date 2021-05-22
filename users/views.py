from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from users.forms import FormRegisto, GestorAuthenticationForm
# Create your views here.

def home_view(request):
    return render(request,'home.html')

def teste_view(request):
    return render(request,'base.html')

def register_view(request):
    context = {}
    if request.POST:
        form = FormRegisto(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email = email, password=raw_password)
            login(request,user)
            return redirect('home')
        else:
            context['form_registo']  = form
    else:
        form = FormRegisto()
        context['form_registo'] = form
    return render(request, 'register.html',context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    
    context = {}
    user = request.user
    if user.is_authenticated:
        
        return redirect("home")
    if request.POST:        
        form = GestorAuthenticationForm(request.POST)
        context['login_form'] = form
        if form.is_valid():            
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email = email, password = password)            
            if user:                
                login(request,user)
                return redirect("home") 
        
    else:        
        form = GestorAuthenticationForm()
        
    context['login_form'] = form
    return render(request, "login.html",context)

