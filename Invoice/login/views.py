from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,auth


# some stuff here specific to your app


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['passwd']
        user= auth.authenticate(username=username,password=passwd)
        if user is not None:
            auth.login(request,user)
            return redirect('/home')
        else:
            messages.info(request,'passwd')
            return redirect('/')
    else:
        if request.user.is_authenticated:
            return redirect('/home')
        else:
            users = User.objects.all()
            return render(request,'index.html',{'Users':users,'name':'Mughal Invoice'})
