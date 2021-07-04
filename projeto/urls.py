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
from users.views import *
from caixas.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page_view, name = "home"),
    path('registo/', register_view, name ="registo"),
    path('logout/', logout_view, name ="logout"),
    path('login/', login_view, name ="login"),    
    path('associar/cartoes_pessoas', associar_pessoa_cartao_view, name="associar_pessoa_cartao"),
    
    path('locais/adicionar', locais_view, name ="locais"),
    path('locais/editar/<int:id>',local_editar_view, name ="locais_editar"),
    path('locais/<int:id>',local_details_view, name="local_details"),

    path('pessoas/adicionar', pessoas_view, name ="pessoas"),
    path('pessoas/detalhes/<int:id>',pessoa_details_view, name = "pessoa_detalhes"),
    
    path('registos/', registos_view, name ="registos"),
    path('cartoes/adicionar', adicionar_cartao, name ="cartoes"),
    path('cartoes/detalhes/<int:id>', cartoes_details_view, name ="cartoes_detalhes"),
    path('cartoes/editar/<int:id>', cartoes_editar_view, name ="cartoes_editar"),
    path('pessoas/editar/<int:id>', pessoas_editar_view, name ="pessoas_editar"),    
    
    
    
    path('pessoas/lista',lista_pessoas_view,name ="lista_pessoas"),
    path('cartoes/lista',lista_cartoes_view,name ="lista_cartoes"),
    path('presencas.php',dados_caixas_view,name = "dados_caixas"),
    path('pdf',generate_pdf,name="pdf"),
    path('relacoes_edf_gestores/historico',historico_rel_edf_gestores,name="historico_rel"),

    path('caixas/detalhes/<int:id>', caixa_details_view,name="caixa_detalhes"),
    path('caixas/inativas',caixas_inativas, name = "caixas_inativas"),    
    path('caixas/adicionar',adicionar_caixa_view, name = "adicionar_caixa"),
    path('caixas/editar/<int:id>',caixas_editar_view, name ="caixas_editar"),
    path('caixas/<int:id_local>', caixas_view_ids,  name= "caixas_ids"),
    path('caixas/', caixas_view, name ="caixas"),
    path('caixas/associar', caixas_associar_local, name ="associar_caixas_local"),
    path('ativar_caixa/<int:caixa_id>',ativar_caixa,name ="ativar_caixa"),
    path('desativar_caixa/<int:caixa_id>',desativar_caixa,name ="desativar_caixa"),

    path('gestores/adicionar', gestores_adicionar_view, name ="gestores_adicionar"),
    path('gestores/lista', gestores_lista, name ="gestores_lista"),
    path('gestores/associar', gestores_associar_edf_view, name="gestores_associar_edf"),
    path('gestores/editar/<int:id>', gestores_editar_view,name = "gestores_editar"),
    path('gestores/detalhes/<int:id>',gestores_details_view,name="gestor_detalhes"),

    path('edificios/', edf_geral_view, name ="edificios"),
    path('edificios/lista/', edf_lista_view, name="lista_edf"),
    path('edificios/historico/', historico_edf_view, name = "edf_historico" ),
    path('edificios/historico/<int:id>', historico_edf_id_view, name = "edf_historico_id" ),
    path('edificios/<int:id>', edificio_details_view, name = "edf_details"),    
    path('edificios/adicionar',adicionar_edf,name="adicionar_edf"),
    path('edificios/editar/<int:id>',editar_edf,name="editar_edf"),
]
