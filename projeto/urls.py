"""projeto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import home_view, register_view, logout_view,login_view
from caixas.views import teste_view, input_view,gestores_view, locais_view ,pessoas_view,edificio_view,gestores_editar,local_editar_view
from caixas.views import cartoes_view, caixas_view, adicionar_caixa_view, pessoas_editar_view, cartoes_editar_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name = "home"),
    path('registo/', register_view, name ="registo"),
    path('logout/', logout_view, name ="logout"),
    path('login/', login_view, name ="login"),
    path('teste/', teste_view, name ="teste"),
    path('input/', input_view, name ="input"),
    path('gestores/adicionar', gestores_view, name ="gestores"),
    path('gestores/editar', gestores_editar, name ="gestores_editar"),
    path('caixas/', caixas_view, name ="caixas"),
    path('locais/', locais_view, name ="locais"),
    path('locais/editar/<int:id>',local_editar_view, name ="locais_editar"),
    path('edificios/', edificio_view, name ="edificios"),
    path('pessoas/', pessoas_view, name ="pessoas"),
    path('relatorios/', home_view, name ="relatorios"),
    path('cartoes/', cartoes_view, name ="cartoes"),
    path('caixas/adicionar',adicionar_caixa_view, name = "adicionar_caixa"),
    path('cartoes/editar/<int:id>', cartoes_editar_view, name ="cartoes_editar"),
    path('pessoas/editar/<int:id>', pessoas_editar_view, name ="pessoas_editar"),
]
