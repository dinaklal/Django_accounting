from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from company.models import Company,Rate,DelNote
from login.models import Sites
from home.models import Invoice,Invoice_Details
from django.contrib import messages
from datetime import datetime
from home.utils import render_to_pdf #created in step 4
from django.views.generic import View
from django.http import HttpResponse
from num2words import num2words
# Create your views here.
from django.db.models import Max


def home(request):
    company = Company.objects.all()
    del_notes = DelNote.objects.filter(invoiced = False)
    un_del  = del_notes.count()
    del_date  = del_notes.aggregate(Max('date'))['date__max']
    
    sites = Sites.objects.all()
    rates = Rate.objects.all()
    today = datetime.today()
    month_start = today.replace(day=1)
    today = today.strftime("%Y-%m-%d")
    month_start = month_start.strftime("%Y-%m-%d")
    return render(request,'home.html',{'sites':sites,'company':company,'rates':rates,'today':today,'month_start':month_start,'un_del':un_del,'del_date':del_date})
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
    company = request.POST['company']
    site = request.POST['site']
    service = request.POST['service']
    from_date = post_data['from_date'][0]
    to_date = post_data['to_date'][0]
    discount = post_data['discount'][0]
    today=datetime.today()
    today = today.strftime("%Y-%m-%d")

    if site == 'all' and service  == 'all':

        del_notes = DelNote.objects.filter(company_id=company,invoiced = False,date__range=(from_date, to_date))

    elif service =='all' and site != 'all':

        del_notes = DelNote.objects.filter(company_id=company,site_id = site,invoiced = False,date__range=(from_date, to_date))

    elif site == 'all' and service != 'all':
        del_notes = DelNote.objects.filter(company_id=company,service = service,invoiced = False,date__range=(from_date, to_date))
    else :
        del_notes = DelNote.objects.filter(company_id=company,service = service,site_id = site,invoiced = False,date__range=(from_date, to_date))
    
    if len(del_notes) == 0 :
        print(len(del_notes))
        messages.error(request,'duplicate')
        return render(request,'invoice_added.html')
    else:
        ob = Invoice(company_id = company,amount = 0, discount = discount,date =today)
        ob.save()
        tot_price = 0.0
        inv_print = []
        inv = {}    
        for del_note in del_notes:   
            
            rate = Rate.objects.get(company_id = del_note.company_id, site_id = del_note.site_id)        
            ob1 = Invoice_Details(inv_id =ob.id ,del_note_id  = del_note.id, rate_id = rate.id )
            ob1.save()
            site_ob = Sites.objects.get(id = del_note.site_id)

            
            inv['site_id'] = site_ob.id
            inv['site'] = site_ob.name
            

            if del_note.units == '1' and del_note.service == 's1':
                tot = float(del_note.units) * float(rate.service2)
                inv['sum'] = float(del_note.units) * float(rate.service2)
                inv['unit_price'] = rate.service2
                inv['units'] = 1
                inv['service'] = 'Sweet Water (in Trips)'
            elif del_note.service == 's1':            
                tot = float(del_note.units) * float(rate.service1)
                inv['sum'] = float(del_note.units) * float(rate.service1)
                inv['unit_price'] = rate.service1
                inv['units'] = int(del_note.units)
                inv['service'] = 'Sweet Water (in Gallon)'
            else:
                tot = float(del_note.units) * float(rate.service3)
                inv['sum'] = float(del_note.units) * float(rate.service3)
                inv['unit_price'] = rate.service3                
                inv['units'] = 1
                inv['service'] = 'Sewage Water Removal (in Trips)'
            tot_price =  tot + tot_price
            del_note.invoiced = True
            del_note.inv_id = ob.id
            del_note.save()
            flag  = False
            for i in range (len(inv_print)):
                if inv_print[i]['site_id'] == inv['site_id'] and inv_print[i]['service'] == inv['service']:
                    flag = True
                    inv_print[i]['sum'] = float(inv_print[i]['sum'])+ float( inv['sum'])
                    inv_print[i]['units'] = int(inv_print[i]['units'])  +  int(inv['units'])
            if flag == False:
                inv_print.append(inv)
            inv = {}
        ob.amount = tot_price
        ob.save()        
        company_data  = Company.objects.get(id=company)
        company_data.total = tot_price
        company_data.total1 = tot_price - float(discount)
        company_data.discount = discount
        company_data.inv = ob.id
        company_data.date = ob.date
        #print(inv_print)
        return render(request,'invoice_added.html',{'invoice':inv_print,'company':company_data})

def GeneratePdf(request):
        get_data = dict(request.GET.lists())
        id=get_data['inv_id'][0]
        invoice = Invoice.objects.get(id=id)
        sales =   Invoice_Details.objects.filter(inv_id=id)
        inv_print = []
        i=1
        tot_price = 0.0
        inv_print = []
        inv = {}   
        for sale in sales:
            del_note = DelNote.objects.get(id = sale.del_note_id)
            rate = Rate.objects.get(id = sale.rate_id)
            site_ob = Sites.objects.get(id = del_note.site_id)            
            inv['site_id'] = site_ob.id
            inv['site'] = site_ob.name      

            if del_note.units == '1' and del_note.service == 's1':
                tot = float(del_note.units) * float(rate.service2)
                inv['sum'] = float(del_note.units) * float(rate.service2)
                inv['unit_price'] = rate.service2
                inv['units'] = 1
                inv['service'] = 'Sweet Water (in Trips)'
            elif del_note.service == 's1':            
                tot = float(del_note.units) * float(rate.service1)
                inv['sum'] = float(del_note.units) * float(rate.service1)
                inv['unit_price'] = rate.service1
                inv['units'] = int(del_note.units)
                inv['service'] = 'Sweet Water (in Gallon)'
            else:
                tot = float(del_note.units) * float(rate.service3)
                inv['sum'] = float(del_note.units) * float(rate.service3)
                inv['unit_price'] = rate.service3                
                inv['units'] = 1
                inv['service'] = 'Sewage Water Removal (in Trips)'
            tot_price =  tot + tot_price
            flag  = False
            for i in range (len(inv_print)):
                if inv_print[i]['site_id'] == inv['site_id'] and inv_print[i]['service'] == inv['service']:
                    flag = True
                    inv_print[i]['sum'] = float(inv_print[i]['sum'])+ float( inv['sum'])
                    inv_print[i]['units'] = int(inv_print[i]['units'])  +  int(inv['units'])
            if flag == False:
                inv_print.append(inv)
            inv = {}           
        company_data  = Company.objects.get(id=invoice.company_id)
        invoice.total1 = float(invoice.amount) - float(invoice.discount) 
        invoice.words = num2words(invoice.total1)
        pdf = render_to_pdf('invoice.html',{ 'invoice':invoice,'sales':inv_print,'invoice1':company_data})
        return HttpResponse(pdf, content_type='application/pdf')           
def get_invoice(request):   
    invoice = Invoice.objects.all().order_by('-date')[:5]
    for i in invoice:
        i.inv = "#"+str(i.id)
        i.company = Company.objects.get(id = i.company_id).name
    today=datetime.today()
    today = today.strftime("%Y-%m-%d")
    #print(today)
    return render(request,'view_inv.html',{'invoice':invoice,'date':today})
def edit_inv_date(request):   
    post_data = dict(request.POST.lists())
    post_data.pop('csrfmiddlewaretoken',None)
    from_date = post_data['from_date'][0]
    to_date = post_data['to_date'][0]

    invoice = DelNote.objects.filter(date__range=(from_date, to_date))
    for i in invoice:
        i.company = Company.objects.get(id = i.company_id).name
        i.site = Sites.objects.get(id = i.site_id).name
        i.inv_id = "Nill" if i.inv_id == 0 else "#"+str(i.inv_id)
        i.service = "Sweet Water supply" if i.service == 's1' else "Sewage Water removal"
    return render(request,'view_inv_date.html',{'invoice':invoice,'date':to_date,'from_date':from_date})
def edit_inv(request):
    inv_id = request.POST['inv_id']
    invoice = Invoice.objects.get(id= inv_id)
    inv_detail = Invoice_Details.objects.filter(inv_id = inv_id)   
    company = Company.objects.get(id=invoice.company_id)
    company.inv_id = inv_id
    notes = []
    element = {}
    i=1
    tot_trips = 0
    tot_units = 0
    tot_price = 0
    for inv_det in inv_detail:
        del_note = DelNote.objects.get(id = inv_det.del_note_id)
        element['id']= del_note.id
        i = i+1
        element['del_id'] = del_note.del_note_id
        element['site_id'] = del_note.site_id
        site = Sites.objects.get(id=del_note.site_id)
        element['site_name'] = site.name
            
        rate = Rate.objects.get(company_id = del_note.company_id, site_id = del_note.site_id)
        if del_note.units == '1' and del_note.service == 's1':
            element['u_price'] = rate.service2
            element['trip'] = 1
            element['service'] = "Sweet Water "
            element['total_price'] = float(del_note.units) * float(rate.service2)
            element['units'] = del_note.units + ' Trip'
            tot_trips += 1
                
            tot_price =  element['total_price'] + tot_price
        elif del_note.service == 's1':
            element['u_price'] = rate.service1
            element['trip'] = 0
            element['service'] = "Sweet Water "
            element['total_price'] = float(del_note.units) * float(rate.service1)
            tot_price =  element['total_price'] + tot_price
            element['units'] = del_note.units + ' Gallon'
            tot_units = tot_units +  int(del_note.units)

        else:
            element['u_price'] = rate.service3
            element['trip'] = 1
            tot_trips += 1
            element['total_price'] = float(del_note.units) * float(rate.service3)
    
            tot_price =  element['total_price'] + tot_price
            element['service'] = "Sewage Water Removal"
            element['units'] = del_note.units + ' Trip'
        element['veh_no'] = del_note.veh_no
        
        element['date'] = del_note.date
        notes.append(element)
        element = {}
    notes = sorted(notes, key=lambda k: k['trip']) 
    company.tot_price  = tot_price
    company.tot_units = tot_units
    company.tot_trips = tot_trips
        #today = post_data['to_date']
    sites = Sites.objects.all()
    rates = Rate.objects.all()
        
    today=datetime.today()
    today = today.strftime("%Y-%m-%d")
    return render(request,'edit_inv.html',{'company':company,'sites':sites,'rate':rates,'today':today,'del_notes':notes,'discount':invoice.discount})

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
