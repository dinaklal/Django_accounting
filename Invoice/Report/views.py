from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from login.models import Sites
from home.models import Invoice,Invoice_Details
from Report.models import Account
from django.contrib import messages
from company.models import Company
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
    inv_list = []
    for inv in invoice:
        i = inv.company_id
        company = Company.objects.get(id = i)
        inv.customer = company.name
        inv.contact = company.contact
        inv_list.append(inv)
    no_of_rows = invoice.count()
    total_price = invoice.aggregate(Sum('amount'))['amount__sum']
    discount = invoice.aggregate(Sum('discount'))['discount__sum']
    return render(request,'report.html',{'today':today,'month_start':month_start,'invoice':inv_list,'rows':no_of_rows,'total':total_price,'discount':discount})
def add_money(request):
    if not request.POST :
        today = datetime.today()
        today = today.strftime("%Y-%m-%d")
        company = Company.objects.all()
        return render(request,'add_money.html',{'company':company,'today':today})
    else:
        post_data = dict(request.POST.lists())
        post_data.pop('csrfmiddlewaretoken',None)
        date = post_data['date'][0]
        com_id = post_data['company'][0]
        amount  = post_data['amount'][0]
        ob = Account(from_company = com_id,amount = amount,date =date)
        ob.save()
        messages.info(request,'done')
        return redirect('add_money')
def summary(request):
    if not request.GET :
        today = datetime.today()
        today = today.strftime("%Y-%m-%d")
        company = Company.objects.all()
        c= []
        for com in company:
            invoice = Invoice.objects.filter(company_id = com.id)
            if invoice.count() > 0:
                total_price = invoice.aggregate(Sum('amount'))['amount__sum'] - invoice.aggregate(Sum('discount'))['discount__sum']
            else: 
                total_price = 0
            com.tot =  total_price  + com.starting_balance
                 
            money = Account.objects.filter(from_company = com.id)
            if money.count() > 0:
                total_price = money.aggregate(Sum('amount'))['amount__sum']
            else: 
                total_price = 0
            com.m = total_price
            com.b = com.tot - com.m
            c.append(com)
        total_price = Invoice.objects.all().aggregate(Sum('amount'))['amount__sum'] 
        tot_b = Invoice.objects.all().aggregate(Sum('discount'))['discount__sum']
        tot_m = Account.objects.all().aggregate(Sum('amount'))['amount__sum']
        tot = {}
        tot['in'] = Invoice.objects.all().count()
        tot['price'] = total_price
        tot['dis'] = tot_b
        tot['m'] = tot_m
        if total_price != None and tot_b != None and tot_m != None:
         tot['b']=  total_price - tot_b - tot_m
        return render(request,'summary.html',{'company':c,'today':today,'tot':tot})
    else:
        comp_id = request.GET['company_id']
        tot ={}
        company = Company.objects.get(id = comp_id)
        tot['name'] = company.name
        amount = Account.objects.filter(from_company = comp_id).order_by('date')
        invoice = Invoice.objects.filter(company_id = comp_id).order_by('date') 
        i=0
        j=0 
        c=[]
        ele ={}
        tot_it = company.starting_balance
        ele['type'] = 'Debit'
        ele['Description'] = 'Starting Balance'
        ele['amount'] = company.starting_balance
        ele['total_amount'] = company.starting_balance
        c.append(ele)
        tot_cre = 0.0
        tot_deb = float(company.starting_balance)
        while i < amount.count() and j <  invoice.count():
            if amount[i].date < invoice[j].date:
                ele ={}
                ele['type'] = 'Credit'
                ele['Description'] = 'Amount from Company'
                ele['amount'] = amount[i].amount
                tot_it = round(float(tot_it) - float(amount[i].amount),5)
                tot_cre = tot_cre + float(amount[i].amount)
                ele['total_amount'] = tot_it 
                ele['date'] = amount[i].date
                c.append(ele)
                i = i+1
            else:
                ele ={}
                ele['type'] = 'Debit'
                ele['Description'] = 'Invoiced - #'+str(invoice[j].id)
                ele['amount'] = invoice[j].amount
                tot_deb = tot_deb + float(invoice[j].amount)
                tot_it = round(float(tot_it) + float(invoice[j].amount)  - float(invoice[j].discount),5)
                ele['total_amount'] = tot_it 
                ele['date'] = invoice[j].date
                c.append(ele)
                j=j+1
        while i <  amount.count():
            ele ={}
            ele['type'] = 'Credit'
            ele['Description'] = 'Amount from Company'
            ele['amount'] = amount[i].amount
            tot_cre = tot_cre + float(amount[i].amount)
            tot_it = round(float(tot_it) - float(amount[i].amount),5)
            ele['total_amount'] = tot_it 
            ele['date'] = amount[i].date
            c.append(ele)
            i = i+1
        while j <  invoice.count():
            ele ={}
            ele['type'] = 'Debit'
            ele['Description'] = 'Invoiced - #'+str(invoice[j].id)
            ele['amount'] = invoice[j].amount
            tot_deb = tot_deb + float(invoice[j].amount)
            tot_it = round (float(tot_it) + float(invoice[j].amount) - float(invoice[j].discount),5)
            ele['total_amount'] = tot_it 
            ele['date'] = invoice[j].date
            c.append(ele)
            j = j+1
        


        #print(tot)
        if len(c) > 1 :
            t = c[1]['date'].strftime("%Y-%m-%d")
        else:
            t = datetime(2020, 1, 1).strftime("%Y-%m-%d")
        tot['tot_cred'] = round(float(tot_cre),5)
        tot['tot_deb'] = round(float(tot_deb),5)
        tot['tot_bal'] = tot['tot_deb'] - tot['tot_cred'] 
        print(tot)
        tot['price']= invoice.aggregate(Sum('amount'))['amount__sum'] 
        tot['start_price'] = company.starting_balance
        tot['in']= invoice.count()
        tot['dis'] = invoice.aggregate(Sum('discount'))['discount__sum'] 
        tot['m'] = amount.aggregate(Sum('amount'))['amount__sum'] 
        if tot['price'] != None and tot['dis']  != None and tot['m'] != None:
            tot['b']= round( tot['price']- tot['dis'] - tot['m'] +  company.starting_balance,5)
        return render(request,'summary1.html',{'amount':c,'tot':tot,'company':company,'date':t})
def add_start(request):
    if not request.POST :
        today = datetime.today()
        today = today.strftime("%Y-%m-%d")
        company = Company.objects.all()
        return render(request,'add_start_balance.html',{'company':company,'today':today})
    else:
        post_data = dict(request.POST.lists())
        post_data.pop('csrfmiddlewaretoken',None)
        com_id = post_data['company'][0]
        amount  = post_data['amount'][0]
        ob = Company.objects.get(id=com_id)
        ob.starting_balance = amount
        ob.save()
        messages.info(request,'done')
        return redirect('add_start')
    
def print_account(request):
    post_data = dict(request.POST.lists())
    post_data.pop('csrfmiddlewaretoken',None)
    date = post_data['date'][0]
    comp_id  = post_data['company'][0]
    tot ={}
    company = Company.objects.get(id = comp_id)
    tot['name'] = company.name
    amount = Account.objects.filter(from_company = comp_id).order_by('date')
    invoice = Invoice.objects.filter(company_id = comp_id).order_by('date') 
    i=0
    j=0 
    c=[]
    f = []
    ele ={}
    tot_it = company.starting_balance
    ele['type'] = 'Debit'
    ele['Description'] = 'Starting Balance'
    ele['amount'] = company.starting_balance
    ele['total_amount'] = company.starting_balance
    c.append(ele)
    f.append(ele)
    tot_cre = 0.0
    tot_deb = float(company.starting_balance)
    while i < amount.count() and j <  invoice.count():
        if amount[i].date < invoice[j].date:
            
            ele ={}
            ele['type'] = 'Credit'
            ele['Description'] = 'Amount from Company'
            ele['amount'] = amount[i].amount
            tot_it = round(float(tot_it) - float(amount[i].amount),5)
            tot_cre = tot_cre + float(amount[i].amount)
            ele['total_amount'] = tot_it 
            ele['date'] = amount[i].date
            c.append(ele)
            i = i+1
        else:
            ele ={}
            ele['type'] = 'Debit'
            ele['Description'] = 'Invoiced - #'+str(invoice[j].id)
            ele['amount'] = invoice[j].amount
            tot_deb = tot_deb + float(invoice[j].amount)
            tot_it = round(float(tot_it) + float(invoice[j].amount)  - float(invoice[j].discount),5)
            ele['total_amount'] = tot_it 
            ele['date'] = invoice[j].date
            c.append(ele)
            j=j+1
    while i <  amount.count():
        ele ={}
        ele['type'] = 'Credit'
        ele['Description'] = 'Amount from Company'
        ele['amount'] = amount[i].amount
        tot_cre = tot_cre + float(amount[i].amount)
        tot_it = round(float(tot_it) - float(amount[i].amount),5)
        ele['total_amount'] = tot_it 
        ele['date'] = amount[i].date
        c.append(ele)
        i = i+1
    while j <  invoice.count():
        ele ={}
        ele['type'] = 'Debit'
        ele['Description'] = 'Invoiced - #'+str(invoice[j].id)
        ele['amount'] = invoice[j].amount
        tot_deb = tot_deb + float(invoice[j].amount)
        tot_it = round (float(tot_it) + float(invoice[j].amount) - float(invoice[j].discount),5)
        ele['total_amount'] = tot_it 
        ele['date'] = invoice[j].date
        c.append(ele)
        j = j+1

    tot_cre = 0.0
    tot_deb = float(f[0]['amount'])
    for i in range(1,len(c)):
        if c[i]['date'] < datetime.strptime(date, '%Y-%m-%d').date() :            
            if c[i]['type'] == 'Debit':
                f[0]['amount'] = float(f[0]['amount']) + float(c[i]['amount'])
            else:
                f[0]['amount'] = float(f[0]['amount']) - float(c[i]['amount'])
            tot_deb = float(f[0]['amount'])
        else:
            f.append(c[i])
            if c[i]['type'] == 'Debit':
                tot_deb = tot_deb + float(c[i]['amount'])
            else:
                tot_cre = tot_cre + float(c[i]['amount'])

    #print(c)
    tot['tot_cred'] = round(float(tot_cre),5)
    tot['tot_deb'] = round(float(tot_deb),5)
    tot['tot_bal'] = tot['tot_deb'] - tot['tot_cred'] 
  
    tot['price']= invoice.aggregate(Sum('amount'))['amount__sum'] 
    tot['start_price'] = company.starting_balance
    tot['in']= invoice.count()
    tot['dis'] = invoice.aggregate(Sum('discount'))['discount__sum'] 
    tot['m'] = amount.aggregate(Sum('amount'))['amount__sum'] 
    if tot['price'] != None and tot['dis']  != None and tot['m'] != None:
        tot['b']= round( tot['price']- tot['dis'] - tot['m'] +  company.starting_balance,5)
    pdf = render_to_pdf('account_print.html',{ 'date':date, 'tot':tot,'amount':f,'company':company})
    return HttpResponse(pdf, content_type='application/pdf') 
