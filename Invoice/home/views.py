from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from company.models import Company,Rate
from login.models import Sites
from home.models import Invoice,Sales
from django.contrib import messages
from datetime import datetime
from home.utils import render_to_pdf #created in step 4
from django.views.generic import View
from django.http import HttpResponse
# Create your views here.


def home(request):
    sites= Sites.objects.all()
    return render(request,'home.html',{'sites':sites})
def logout(request):
    auth.logout(request)
    return redirect('/')
def add_site(request):
    if request.method == 'POST':
        name = request.POST['name']
        company = request.POST['company']
        s1 = request.POST['s1']
        s2 = request.POST['s2']
        s3 = request.POST['s3']
        desc = request.POST['desc']
        if Sites.objects.filter(name=name).exists():
            messages.error(request,'duplicate')
            return redirect('add_site')
        else:
            ob=Sites(name=name,Description=desc)
            ob.save()
            site_id = ob.id
            ob=Rate(company_id=company,site_id=site_id,service1 = s1,service2 = s2,service3 = s3)
            ob.save()
            messages.info(request,'done')
            return redirect('add_site')
    else:
        companies =  Company.objects.all()
        return render(request,'add_site.html',{'companies':companies})
def view_site(request):
    sites= Sites.objects.all()
    return render(request,'view_site.html',{'sites':sites})
def process(request):
    post_data = dict(request.POST.lists())
    post_data.pop('csrfmiddlewaretoken',None)
    total= post_data['total_amount'][0]
    discount = post_data['discount'][0]
    total_units=  post_data['tot_units'][0]
    customer = post_data['customer'][0]
    contact = post_data['contact'][0]
    address = post_data['address'][0]
    date=post_data['date'][0]
    date = datetime.strptime(date, "%Y/%m/%d")
    #print(total)    
    ob = Invoice(customer=customer,address=address,contact=contact,discount=discount,total_price=total,total_units=total_units,date=date)
    ob.save()
    inv_id = Invoice.objects.latest('id').id
    if discount == '':
        discount = "0"
    invoice  = {'date':date,'name':customer,'address':address,'id':inv_id,'discount':float(discount),'contact':contact,'total':total,'tot_units':total_units,'to':float(total)+float(discount)}   
    sale = []
    sn={}
    i=1
    for key in post_data:
        
        if key.startswith('selid'):
            site_id = post_data[key][0]
            s= Sites.objects.get(id=site_id)
            sn['name']=s.name
            sn['uprice']=s.Unit_price
        if key.startswith('sel1id'):
            units_load= post_data[key][0]
            sn['uload']=units_load
        if key.startswith('lodid'):
            no_loads = post_data[key][0]
            sn['loads']=no_loads
        if key.startswith('untid'):
            tot_units = post_data[key][0]
            sn['units']=tot_units
        if key.startswith('totid'):
            sn['sino']=i
            i=i+1
            tot_price = post_data[key][0]
            sn['price']=tot_price
            
            sale.append(sn)
            sn={}
            ob= Sales(inv_id=inv_id,site_id=site_id,units_load=units_load,no_loads=no_loads,tot_units=tot_units,tot_price=tot_price)
            ob.save()
        
    
    print(sn)
    return render(request,'invoice_added.html',{'invoice':invoice,'sales':sale})

def GeneratePdf(request):
        get_data = dict(request.GET.lists())
        id=get_data['inv_id'][0]
        invoice = Invoice.objects.get(id=id)
        sales= list(Sales.objects.filter(inv_id=id))
        sal = []
        sn={}
        i=1
        for sale in sales:
            s= Sites.objects.get(id=sale.site_id)
            sn['name']=s.name
            sn['uprice']=s.Unit_price
            sn['uload']=sale.units_load
            sn['loads']=sale.no_loads
            sn['units']=sale.tot_units
            sn['sino']=i
            i=i+1
            sn['price']=sale.tot_price
            
            sal.append(sn)
            sn={}
        if invoice.discount == '':
            invoice.discount = "0"
        to=float(invoice.total_price)+float(invoice.discount)
        pdf = render_to_pdf('invoice.html',{ 'invoice':invoice,'sales':sal,'to':to})
        return HttpResponse(pdf, content_type='application/pdf')           
def get_invoice(request):   
    invoice = Invoice.objects.all().order_by('-date')[:5]
    today=datetime.today()
    today = today.strftime("%Y-%m-%d")
    print(today)
    return render(request,'view_inv.html',{'invoice':invoice,'date':today})
def edit_inv_date(request):   
    post_data = dict(request.POST.lists())
    post_data.pop('csrfmiddlewaretoken',None)
    from_date = post_data['from_date'][0]
    to_date = post_data['to_date'][0]
    invoice = Invoice.objects.filter(date__range=(from_date, to_date))
    return render(request,'view_inv_date.html',{'invoice':invoice,'date':to_date,'from_date':from_date})
def edit_inv(request):
    post_data = dict(request.POST.lists())
    post_data.pop('csrfmiddlewaretoken',None)
    id = post_data['inv_id'][0]
    invoice = Invoice.objects.get(id=id)
    #print(invoice)
    sales= list(Sales.objects.filter(inv_id=id))
    sal = []
    sn={}
    i=1
    for sale in sales:
            s= Sites.objects.get(id=sale.site_id)
            sn['name']=s.name
            sn['uprice']=s.Unit_price
            sn['uload']=sale.units_load
            sn['loads']=sale.no_loads
            sn['units']=sale.tot_units
            sn['sino']=i
            i=i+1
            sn['price']=sale.tot_price
            sn['id']=sale.id
            
            sal.append(sn)
            sn={}
    if invoice.discount == '':
            invoice.discount = "0"
    to=float(invoice.total_price)+float(invoice.discount)
    print(invoice)
    invoice.date = invoice.date.strftime("%Y-%m-%d")
    return render(request,'edit_inv.html',{ 'invoice':invoice,'sales':sal,'to':to})

def save_inv(request):
    post_data = dict(request.POST.lists())
    post_data.pop('csrfmiddlewaretoken',None)

    print(post_data)
    inv_id=post_data['inv_id'][0]
    customer = post_data['name'][0]
    address = post_data['address'][0]
    contact = post_data['contact'][0]
    total_price = post_data['total'][0]
    discount = post_data['discount'][0]
    date = post_data['date'][0]
    total_units=post_data['tot_units'][0]

    if '_print' in request.POST:
        ob=Invoice.objects.get(id=inv_id)
        ob.customer = customer
        ob.address = post_data['address'][0]
        ob.contact = post_data['contact'][0]
        ob.total_price = post_data['total'][0]
        ob.discount = post_data['discount'][0]
        ob.date = post_data['date'][0]
        ob.total_units=post_data['tot_units'][0]

        invoice  = {'date':ob.date,'name':ob.customer,'address':ob.address,'id':inv_id,'discount':float(ob.discount),'contact':ob.contact,'total':ob.total_price,'tot_units':ob.total_units,'to':float(ob.total_price)+float(ob.discount)}   
        
        ob.save()
        #Sales.objects.filter(inv_id=inv_id).delete()
        sale1=[]
        sn  = {}
        i=1
        for key in post_data:
            
            if key.startswith('salea'):
                site_name = post_data[key][0].split('/')
                site_id = Sites.objects.filter(name=site_name[0])
                sn['name']=site_id[0].name
                sn['uprice']=site_id[0].Unit_price
                #print(site_id[0].name)
                if not site_id :
                    break;#print("site Name didnt macthed")
                else:
                    print(site_id[0].name)
            if key.startswith('saleb'):
                loads = post_data[key][0].split('*')           
                #print(loads[1])
                #print(loads[0])
            if key.startswith('sale_id'):
                sale_id = post_data[key][0]

                sale = Sales.objects.get(id=sale_id)
                sale.inv_id = inv_id
                sale.site_id = site_id[0].id
                sale.units_load = loads[0]
                sn['uload']=sale.units_load
                sale.no_loads = loads[1]

                sn['loads']=sale.no_loads
                sale.tot_units = int(loads[0]) * int(loads[1])

                sn['units']=sale.tot_units
                sn['sino']=i
                i = i +1
            
                sale.tot_price = int(loads[0]) * int(loads[1]) * int(site_id[0].Unit_price)
                sn['price']=sale.tot_price
                sale1.append(sn)
                sale.save()
                sn={}
        return render(request,'save_inv.html',{ 'inv_id':int(inv_id),'invoice':invoice,'sales':sale1})
    else :
        #print(post_data)

        invoice  = {'date':date,'name':customer,'address':address,'id':inv_id,'discount':float(discount),'contact':contact,'total_price':total_price,'total_units':total_units,'to':float(total_price)+float(discount)}   
        
        print(invoice)    
        sale1=[]
        sn  = {}
        i=1
        for key in post_data:
            
            if key.startswith('salea'):
                site_name = post_data[key][0].split('/')
                sn['name']=site_name[0]
                sn['uprice']=site_name[1]
                #print(site_id[0].name)
                
            if key.startswith('saleb'):
                loads = post_data[key][0].split('*')           
                sn['uload']=loads[0]
                sn['loads']=loads[1]
            if key.startswith('salec'):
                sn['units']=post_data[key][0]
            if key.startswith('saled'):
                sn['price']=post_data[key][0]
            if key.startswith('sale_id'):
                sale_id = post_data[key][0]
                sn['sino']=i
                i = i +1            
                sale1.append(sn)               
                sn={}       
        pdf = render_to_pdf('invoice.html',{ 'invoice':invoice,'sales':sale1,'to':invoice['to']})
        return HttpResponse(pdf, content_type='application/pdf')
