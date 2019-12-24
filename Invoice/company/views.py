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
        name = request.POST['name']
        contact = request.POST['contact']
        address = request.POST['address']
        if Company.objects.filter(name=name).exists():
            messages.error(request,'duplicate')
            return redirect('add_de_note')
        else:
            ob=Company(name=name,contact=contact,address=address)
            ob.save()
            messages.info(request,'done')
            return redirect('add_de_note')
    else:
        company = Company.objects.all()
        sites = Sites.objects.all()
        rates = Rate.objects.all()
        today=datetime.today()
        today = today.strftime("%Y-%m-%d")
        return render(request,'add_de_note.html',{'company':company,'sites':sites,'rate':rates,'today':today})
