from django.http.response import HttpResponse
from django.shortcuts import render
from caixas.models import Local, Registo, Caixa

import datetime
from ..utils import render_to_pdf 


def home_page_view(request):
    context ={}
    labels = []
    data = []
    labels1 = []
    data1 = []

    num_caixas_inativas = Caixa.objects.filter(utilizavel= False).count()
    data1.append(num_caixas_inativas)
    labels1.append("Caixas Inativas")
    num_caixas_ativas = Caixa.objects.filter(utilizavel= True).count()
    data1.append(num_caixas_ativas)
    labels1.append("Caixas Ativas")
    

    queryset = Local.objects.order_by()[:5]
    for x in queryset:
        labels.append(x.nome)
        data.append(Registo.objects.filter(local_atual_caixa = x.nome).count())

    context["data1"] = data1
    context["labels1"] = labels1
    context["labels"] = labels
    context["data"] = data
    return render(request, 'home_page.html',context)

def generate_pdf(request, *args, **kwargs):
    registos = Registo.objects.all()
    context = {         
        'amount': 39.99,
        'customer_name': 'Cooper Mann',
        'order_id': 1233434,
        'registos': registos,
    }
    pdf = render_to_pdf('pdf/relatorio.html', context)
    return HttpResponse(pdf, content_type='application/pdf')