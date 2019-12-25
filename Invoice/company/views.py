from django.shortcuts import render,redirect
from company.models import Company,Rate,DelNote
from login.models import Sites
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
        if Rate.objects.filter(company_id=company,site_id = site ).exists():
           
            ob=DelNote(del_note_id = del_id, veh_no = veh_no,company_id=company,site_id = site, date = date, service = service,units = units ,invoiced = False)
            ob.save()
            messages.info(request,'done')
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
        print(s1)
        if Rate.objects.filter(company_id=company,site_id = site ).exists():
            ob= Rate.objects.get(company_id=company,site_id = site )
            ob.service1 = s1
            ob.service2 = s2
            ob.service3 = s3
            ob.save()
            messages.info(request,'done')
            return redirect('add_de_note')
           
        else:
            ob=Rate(company_id=company,site_id=site,service1 = s1,service2 = s2,service3 = s3)
            ob.save()
            messages.success(request,'done')
            return redirect('add_de_note')
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

        del_notes = DelNote.objects.filter(company_id=company)

    elif service =='all' and site != 'all':

        del_notes = DelNote.objects.filter(company_id=company,site_id = site)

    elif site == 'all' and service != 'all':
        del_notes = DelNote.objects.filter(company_id=company,service = service)
    else :
        del_notes = DelNote.objects.filter(company_id=company,service = service,site_id = site)
    
    company = Company.objects.get(id=company)
    notes = []
    element = {}
    i=1
    for del_note in del_notes:
        element['sino']= i
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
            element['units'] = del_note.units + ' Trip'
        elif del_note.service == 's1':
            element['u_price'] = rate.service1
            element['trip'] = 0
            element['service'] = "Sweet Water "
            element['units'] = del_note.units + ' Gallon'
        else:
            element['u_price'] = rate.service3
            element['trip'] = 0
            element['service'] = "Sewage Water Removal"
            element['units'] = del_note.units + ' Trip'
        element['veh_no'] = del_note.veh_no
        if del_note.invoiced == False:
            element['invoiced'] = '----'
        else:
            element['invoiced'] =  del_note.invoiced
        element['date'] = del_note.date
        notes.append(element)
        element = {}
    
    print(notes)
    today = post_data['to_date']
    sites = Sites.objects.all()
    rates = Rate.objects.all()
    today=datetime.today()
    today = today.strftime("%Y-%m-%d")
    return render(request,'trip_sheet.html',{'company':company,'sites':sites,'rate':rates,'today':today,'del_notes':notes})
