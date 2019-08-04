from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Group_account,User_account,User_history,Schedule

# Create your views here.

def index(request):
    #g = get_object_or_404(Group_account, pk=1)

    #for check in g.members.all() :
    #    print(check.name.username)
    #    print(check.user_money)
    
    return render(request, 'index.html')

def login(request):
    auth.logout(request)
    return render(request, 'login.html')

def home(request):
    user_group= []
    groups = Group_account.objects.all()
    #print(request.user.username)
    for group in groups:
        #print(group.title)
        for member in group.members.all():
            #print(member.name.username)
            if member.name.username == request.user.username:
                user_group.append(group)
    #print(user_group)
    return render(request, 'home.html',{'groups': user_group})

def logout(request):
    auth.logout(request)
    return redirect('/login')

def group(request):
    return render(request, 'group.html')