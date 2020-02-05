from django.shortcuts import render,redirect
from company.models import Company,Rate,DelNote
from login.models import Sites
from home.models import Invoice_Details,Invoice
from home.utils import render_to_pdf 
from django.http import HttpResponse
#from home.models import 
from django.contrib import messages
from datetime import datetime
# Create your views here.
def add_company(request):
    if request.method == 'POST':
        post_data = dict(request.POST.lists())
        post_data.pop('csrfmiddlewaretoken',None)
        name = request.POST['name']
        contact = request.POST['contact']
        address = request.POST['address']
        if Company.objects.filter(name=name).exists():
            messages.error(request,'duplicate')
            return redirect('add_site')
        else:
            ob=Company(name=name,contact=contact,address=address)
            ob.save()
            messages.info(request,'done')
            return redirect('add_site')
    else:
        return render(request,'add_company.html')
def add_de_note(request):
    if request.method == 'POST':
        post_data = dict(request.POST.lists())
        post_data.pop('csrfmiddlewaretoken',None)
        company = request.POST['company']
        site = request.POST['site']
        del_id = request.POST['del_id']

        veh_no = request.POST['veh_no']
        service = request.POST['service']
        units = request.POST['units']
        date = request.POST['date']
        if DelNote.objects.filter(del_note_id = del_id).exists():
            messages.info(request,'duplicate_del')
            return redirect('add_de_note')
        elif Rate.objects.filter(company_id=company,site_id = site ).exists():
           
            ob=DelNote(del_note_id = del_id, veh_no = veh_no,company_id=company,site_id = site, date = date, service = service,units = units ,invoiced = False)
            ob.save()
            messages.success(request,'done')
            return redirect('add_de_note')
           
        else:
            messages.error(request,'duplicate')
            return redirect('add_de_note')
    else:
        company = Company.objects.all()
        sites = Sites.objects.all()
        rates = Rate.objects.all()
        today=datetime.today()
        today = today.strftime("%Y-%m-%d")
        return render(request,'add_de_note.html',{'company':company,'sites':sites,'rate':rates,'today':today})
def add_rate(request):
    if request.method == 'POST':
        post_data = dict(request.POST.lists())
        post_data.pop('csrfmiddlewaretoken',None)
        company = request.POST['company']
        site = request.POST['site']
        s1 = request.POST['s1']
        s2 = request.POST['s2']
        s3 = request.POST['s3']
        #print(s1)
        if Rate.objects.filter(company_id=company,site_id = site ).exists():
            ob= Rate.objects.get(company_id=company,site_id = site )
            ob.service1 = s1
            ob.service2 = s2
            ob.service3 = s3
            ob.save()
            messages.info(request,'done')
            return redirect('add_rate')
           
        else:
            ob=Rate(company_id=company,site_id=site,service1 = s1,service2 = s2,service3 = s3)
            ob.save()
            messages.success(request,'done')
            return redirect('add_rate')
    else:
        company = Company.objects.all()
        sites = Sites.objects.all()
        rates = Rate.objects.all()
        today=datetime.today()
        today = today.strftime("%Y-%m-%d")
        return render(request,'add_rate.html',{'company':company,'sites':sites,'rate':rates,'today':today})

def trip_sheet(request):
    post_data = dict(request.POST.lists())
    post_data.pop('csrfmiddlewaretoken',None)
    company = request.POST['company']
    site = request.POST['site']
    service = request.POST['service']
    from_date = request.POST['from_date']
    to_date = request.POST['to_date']
    if site == 'all' and service  == 'all':

        del_notes = DelNote.objects.filter(company_id=company,invoiced = False,date__range=(from_date, to_date))

    elif service =='all' and site != 'all':

        del_notes = DelNote.objects.filter(company_id=company,site_id = site,invoiced = False,date__range=(from_date, to_date))

    elif site == 'all' and service != 'all':
        del_notes = DelNote.objects.filter(company_id=company,service = service,invoiced = False,date__range=(from_date, to_date))
    else :
        del_notes = DelNote.objects.filter(company_id=company,service = service,site_id = site,invoiced = False,date__range=(from_date, to_date))
    
    company = Company.objects.get(id=company)
    company.from_date =  from_date
    company.to_date  = to_date
    company.service  = service
    company.site  = site
    notes = []
    element = {}
    i=1
    tot_trips = 0
    tot_units = 0
    tot_price = 0
    del_notes = del_notes.order_by('date')
    for del_note in del_notes:
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
    #notes = sorted(notes, key=lambda k: k['trip']) 
    company.tot_price  = tot_price
    company.tot_units = tot_units
    company.tot_trips = tot_trips
   
    today = post_data['to_date']
    sites = Sites.objects.all()
    rates = Rate.objects.all()
    today=datetime.today()
    today = today.strftime("%Y-%m-%d")
    return render(request,'trip_sheet.html',{'company':company,'sites':sites,'rate':rates,'today':today,'del_notes':notes})
def print_tripsheet(request):
    get_data = dict(request.GET.lists())
    company=get_data['company'][0]
    site=get_data['site'][0]
    service=get_data['service'][0]
    from_date=get_data['from_date'][0]
    to_date=get_data['to_date'][0]

    if site == 'all' and service  == 'all':

        del_notes = DelNote.objects.filter(company_id=company,invoiced = False,date__range=(from_date, to_date))

    elif service =='all' and site != 'all':

        del_notes = DelNote.objects.filter(company_id=company,site_id = site,invoiced = False,date__range=(from_date, to_date))

    elif site == 'all' and service != 'all':
        del_notes = DelNote.objects.filter(company_id=company,service = service,invoiced = False,date__range=(from_date, to_date))
    else :
        del_notes = DelNote.objects.filter(company_id=company,service = service,site_id = site,invoiced = False,date__range=(from_date, to_date))
    
    company = Company.objects.get(id=company)
    company.from_date =  from_date
    company.to_date  = to_date
    company.service  = service
    company.site  = site
    notes = []
    element = {}
    i=1
    tot_trips = 0
    tot_units = 0
    tot_price = 0
    del_notes = del_notes.order_by('date')
    for del_note in del_notes:
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
            element['service'] = "Sewage Water"
            element['units'] = del_note.units + ' Trip'
        element['veh_no'] = del_note.veh_no
     
        element['date'] = del_note.date
        notes.append(element)
        element = {}
    #notes = sorted(notes, key=lambda k: k['trip']) 
    company.tot_price  = round(tot_price,2)
    company.tot_units = tot_units
    company.tot_trips = tot_trips
    today = get_data['to_date']
    sites = Sites.objects.all()
    rates = Rate.objects.all()
    today=datetime.today()
    today = today.strftime("%Y-%m-%d")
    company.inv_id = 0
    pdf = render_to_pdf('trip.html',{ 'company':company,'sites':sites,'rate':rates,'today':today,'del_notes':notes})
    return HttpResponse(pdf, content_type='application/pdf') 
def view_company(request):
    company = Company.objects.all()
    return render(request,'view_company.html',{'company':company})
def edit_del_note(request):
    if request.method != 'POST':
        del_notes = DelNote.objects.all().order_by('-date')[:5]
        d = []
        element = {}
        for del_note in del_notes:
            element['id']= del_note.id
            element['del_id'] = del_note.del_note_id
            element['site_id'] = del_note.site_id
            site = Sites.objects.get(id=del_note.site_id)
            element['site_name'] = site.name
            element['company'] = Company.objects.get(id = del_note.company_id).name
            
            if del_note.units == '1' and del_note.service == 's1':
                element['service'] = "Sweet Water "
                element['units'] = del_note.units + ' Trip'
            
            elif del_note.service == 's1':
                element['service'] = "Sweet Water "
                element['units'] = del_note.units + ' Gallon'
            

            else:
                element['service'] = "Sewage Water Removal"
                element['units'] = del_note.units + ' Trip'
            element['veh_no'] = del_note.veh_no
            if del_note.inv_id == 0 :
                element['inv'] = "Nill"
            else:
                element['inv'] = "#"+str(del_note.inv_id )
            element['date'] = del_note.date
            d.append(element)
            element = {}
        today=datetime.today()
        today = today.strftime("%Y-%m-%d")
        #print(today)
        return render(request,'edit_dl_note.html',{'delnote':d,'date':today})
    else:
        post_data = dict(request.POST.lists())
        post_data.pop('csrfmiddlewaretoken',None)
        del_note = DelNote.objects.get(id = request.POST['del_note_id'])
        company = Company.objects.all()
        sites = Sites.objects.all()
        rates = Rate.objects.all()
        del_note.date = del_note.date.strftime("%Y-%m-%d")
        return render(request,'edit_del_note2.html',{'company':company,'sites':sites,'rate':rates,'del_note':del_note})    
def add_de_note2(request):
    if request.method == 'POST':
        post_data = dict(request.POST.lists())
        post_data.pop('csrfmiddlewaretoken',None)
        id = request.POST['id']
        company = request.POST['company']
        site = request.POST['site']
        del_id = request.POST['del_id']
        veh_no = request.POST['veh_no']
        service = request.POST['service']
        units = request.POST['units']
        date = request.POST['date']
        
        if Rate.objects.filter(company_id=company,site_id = site ).exists():
           
            ob=DelNote.objects.get(id = id)
            ob.del_note_id= del_id
            ob.veh_no = veh_no
            ob.company_id=company
            ob.site_id = site
            ob.date = date
            ob.service = service
            ob.units = units 
            try :
                ob.save()
                inv_id = Invoice_Details.objects.filter(del_note_id = id)
                if inv_id:
                    inv_id = inv_id[0].inv_id
                else:
                    inv_id = " "
                messages.success(request,'done')
                return render(request,'edit_del_note2.html',{'inv_id':inv_id})
           
            except:
                messages.info(request,'duplicate_del')
                return redirect('edit_del_note')
            
        else:
            messages.error(request,'duplicate')
            return render(request,'edit_del_note2.html')

def edit_del3(request):
    if request.method == 'POST':
        post_data = dict(request.POST.lists())
        post_data.pop('csrfmiddlewaretoken',None)
        inv_id = request.POST['inv_id']
        inv_date = request.POST['inv_date']
        discount = request.POST['discount']
        del_notes = DelNote.objects.filter(inv_id=inv_id)
        invoice = Invoice.objects.get(id=inv_id)
        invoice.discount = discount
       
        today=datetime.today()
        today = today.strftime("%Y-%m-%d")

        invoice.date = inv_date
        invoice.save()

        if len(del_notes) == 0 :
            print(len(del_notes))
            invoice.delete()
            Invoice_Details.objects.filter(inv_id = inv_id).delete()
            messages.error(request,'duplicate')
            return render(request,'invoice_added.html')
        else:
            tot_price = 0.0
            inv_print = []
            inv = {}  
            for del_note in del_notes:                   
                rate = Rate.objects.get(company_id = del_note.company_id, site_id = del_note.site_id)        
                ob1 = Invoice_Details.objects.get(inv_id =inv_id ,del_note_id  = del_note.id)
                ob1.rate_id = rate.id
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
                del_note.inv_id = inv_id
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
            invoice.amount = tot_price
            invoice.save()        
            company_data  = Company.objects.get(id=invoice.company_id)
            company_data.total = tot_price
            company_data.total1 = tot_price - float(discount)
            company_data.discount = discount
            company_data.inv = invoice.id
            company_data.date = invoice.date
            return render(request,'invoice_added.html',{'invoice':inv_print,'company':company_data})

    else:
        inv_id = request.GET['inv_id']
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
            if del_note.company_id != company.id :
                del_note.invoiced = False
                del_note.inv_id = 0
                del_note.save()
                inv_det.delete()
                continue
            element['id']= del_note.id
            del_note
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
        return render(request,'trip_sheet2.html',{'company':company,'sites':sites,'rate':rates,'today':today,'del_notes':notes,'discount':invoice.discount,'date':invoice.date.strftime("%Y-%m-%d")})

def print_tripsheet_inv (request):
    get_data = dict(request.GET.lists())
    inv_id = get_data['inv_id'][0]
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
        del_note
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
                element['total_price'] = round(float(del_note.units) * float(rate.service2),3)
                element['units'] = del_note.units + ' Trip'
                tot_trips += 1
                
                tot_price =  element['total_price'] + tot_price
        elif del_note.service == 's1':
                element['u_price'] = rate.service1
                element['trip'] = 0
                element['service'] = "Sweet Water "
                element['total_price'] = round(float(del_note.units) * float(rate.service1),3)
                tot_price =  element['total_price'] + tot_price
                element['units'] = del_note.units + ' Gallon'
                tot_units = tot_units +  int(del_note.units)

        else:
                element['u_price'] = rate.service3
                element['trip'] = 1
                tot_trips += 1
                element['total_price'] = round(float(del_note.units) * float(rate.service3),3)
                tot_price =  element['total_price'] + tot_price
                element['service'] = "Sewage Water"
                element['units'] = del_note.units + ' Trip'
        element['veh_no'] = del_note.veh_no
        element['date'] = del_note.date
        notes.append(element)
        element = {}
    notes = sorted(notes, key=lambda k: k['trip']) 
    company.tot_price  = round(tot_price,2)
    company.tot_units = tot_units
    company.tot_trips = tot_trips
        #today = post_data['to_date']
    sites = Sites.objects.all()
    rates = Rate.objects.all()
    today=datetime.today()
    today = today.strftime("%Y-%m-%d")
     
    pdf = render_to_pdf('trip.html',{ 'company':company,'sites':sites,'rate':rates,'today':today,'del_notes':notes})
    return HttpResponse(pdf, content_type='application/pdf') 