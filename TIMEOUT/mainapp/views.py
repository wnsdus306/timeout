from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Group_account,User_account,User_history,Schedule, Invite
from django.conf import settings

def index(request):
    return render(request, 'index.html')


def login(request):
    auth.logout(request)
    return render(request, 'login.html')


def portfolio(request):
    users = User_account.objects.all()

    if request.method == 'POST':
        us = User_account()
        us.name = request.user
        us.user_money = 0
        us.nickname = request.POST['nickname']
        if us.image:
            us.image = request.FILES['image']
        us.save()
        return redirect('/home')
    else:
        for user in users:
            if user.name.username == request.user.username:
                return redirect('/home')
                break
        return render(request, 'portfolio.html')


def home(request):
    users = User_account.objects.all()
    groups = Group_account.objects.all()
    us = User_account()
    user_group= []
    
    for user in users:
        if user.name.username == request.user.username:
            us = User_account.objects.get(name = request.user)
            break

    for group in groups:
        for member in group.members.all():
            if member.name.username == request.user.username:
                user_group.append(group)

    return render(request, 'home.html',{'groups': user_group,'us':us})

    
def invite(request):
    users = User_account.objects.all()
    us = User_account.objects.get(name = request.user)
    group = Group_account()

    if request.method == 'POST':
        group.title = request.POST['gr']
        group.save()
        group.members.add(us)
        group.save()
        for i in range(3):
            invi = 'invite' + str(i+1)
            invitation = Invite()
            invitation.title = request.POST['gr']
            invitation.send = us.nickname
            invitation.receive = request.POST[invi]
            invitation.save()
        return redirect('/home')

    else:
        return render(request, 'invite.html')


def logout(request):
    auth.logout(request)
    return redirect('/login')


def group(request,group_id):
    group = get_object_or_404(Group_account, pk=group_id)
    sche= Schedule.objects.filter(group_ac = group)

    return render(request, 'group.html',{'group' : group, 'schedules': sche})


def newSchedule(request,group_id): 
    return render(request, 'newSche.html')

def create(request):
    schedule = Schedule()

    return redirect('/group/'+str(group.id))


def check(request):
    invitations = Invite.objects.all()
    us = User_account.objects.get(name = request.user)
    invi_us = Invite()

    for invi in invitations:
        if invi.receive == us.nickname:
            invi_us = Invite.objects.get(receive = us.nickname)
            break
            # return render(request, 'check.html', {'invi_us':invi_us})
            # break
    return render(request, 'check.html', {'invi_us':invi_us})
    # return redirect('/home')


def yes(request):
    us = User_account.objects.get(name = request.user)
    invi_us = Invite.objects.get(receive = us.nickname)
    invi_us.check = True
    invi_us.save()
    group = Group_account.objects.get(title = invi_us.title)
    group.title = invi_us.title
    group.save()
    group.members.add(us)
    group.save()
    invi_us.delete()
    
    return redirect('/home')


def no(request):
    us = User_account.objects.get(name = request.user)
    invi_us = Invite.objects.get(receive = us.nickname)
    invi_us.check = False
    invi_us.save()

    return redirect('/home')


def logout(request):
    auth.logout(request)
    return redirect('/login')

