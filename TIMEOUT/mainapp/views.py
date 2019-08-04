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
    users = User_account.objects.all()
    groups = Group_account.objects.all()
    cnt_user = 0 
    cnt_list = []
    us = User_account()
    user_group= []
    
    for user in users:
        cnt_list.append(user)
        if user.name.username == request.user.username:
            us = User_account.objects.get(name = request.user)
            break
        else:
            cnt_user += 1
            
    if cnt_user == len(cnt_list):
        us.name = request.user
        us.user_money = 0
        us.save()

    
    #print(request.user.username)
    for group in groups:
        #print(group.title)
        for member in group.members.all():
            #print(member.name.username)
            if member.name.username == request.user.username:
                user_group.append(group)
    #print(user_group)
    return render(request, 'home.html',{'groups': user_group,'us':us})

def logout(request):
    auth.logout(request)
    return redirect('/login')

def group(request):
    return render(request, 'group.html')