from django.shortcuts import render,redirect
from company.models import Company
from django.contrib import messages

# Create your views here.
def add_company(request):
    if request.method == 'POST':
        post_data = dict(request.POST.lists())
        post_data.pop('csrfmiddlewaretoken',None)
        name = request.POST['name'][0]
        contact = request.POST['contact'][0]
        address = request.POST['address'][0]
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
