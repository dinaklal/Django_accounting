from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from login.models import Sites
from home.models import Invoice,Sales
from django.contrib import messages
from datetime import datetime
from home.utils import render_to_pdf #created in step 4
from django.views.generic import View
from django.http import HttpResponse
# Create your views here.
from django.db.models import Sum

def report(request):
    if not request.POST :
        today = datetime.today()
        month_start = today.replace(day=1)
        today = today.strftime("%Y-%m-%d")
        month_start = month_start.strftime("%Y-%m-%d")
        invoice = Invoice.objects.filter(date__range=(month_start, today))

    else :
        post_data = dict(request.POST.lists())
        post_data.pop('csrfmiddlewaretoken',None)
        month_start = post_data['from_date'][0]
        today = post_data['to_date'][0]
        print(post_data)
        invoice = Invoice.objects.filter(date__range=(month_start, today))
    no_of_rows = invoice.count()
    total_price = invoice.aggregate(Sum('total_price'))['total_price__sum']
    discount = invoice.aggregate(Sum('discount'))['discount__sum']
    total_units = invoice.aggregate(Sum('total_units'))['total_units__sum']
    return render(request,'report.html',{'units':total_units,'today':today,'month_start':month_start,'invoice':invoice,'rows':no_of_rows,'total':total_price,'discount':discount})
