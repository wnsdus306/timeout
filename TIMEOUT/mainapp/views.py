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
    groups = Group_account.objects.all()
    group = Group_account()
    invitation = Invite()
    invitations = Invite.objects.all()
    us_f_list = []
    cnt = 0
    cnt_list =[]
    check = 0

    if request.method == 'POST':

        ############### 동일한 그룹이면 같은멤버 (수정해야함)##############
        for grp in groups:
            cnt_list.append(grp)
            if grp.title != request.POST['gr']:
                cnt += 1

        if cnt == len(cnt_list):
            group.title = request.POST['gr']
            group.save()
            group.members.add(us)
            group.save()
        else:
            group = Group_account.objects.get(title=request.POST['gr'])
        ################################################################
        
        ######################## 초대장 만들기 ##########################
        invitation.title = request.POST['gr']
        invitation.send = us.nickname
        invitation.receive = request.POST['invite']
        invitation.save()
        
        for i in invitations: # 초대장 같은 객체 중복생성 불가
            if i.receive == request.POST['invite'] and i.send == us.nickname and i.title == request.POST['gr']:
                check+=1
                if check != 1:
                    i.delete()
        #################################################################

        invitations_i = Invite.objects.all() # 최종 초대장
        

        for iv in invitations_i:
            if iv.title == request.POST['gr'] and iv.send == us.nickname: # 초대장의 title과 검색한 title이 같으면
                us_f = User_account.objects.get(nickname = iv.receive)
                us_f_list.append(us_f)
                
        return render(request, 'invite.html', {
            'us_f_list':us_f_list,'group':group})

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
    group = get_object_or_404(Group_account,pk=group_id)
    return render(request, 'newSche.html',{'group' : group})

def create(request,group_id):
    schedule = Schedule()
    schedule.group_ac = get_object_or_404(Group_account, pk = group_id)
    schedule.title = request.GET['title']
    schedule.penalty = request.GET['penalty']
    schedule.date = request.GET['date']+" "+request.GET['time']
    schedule.save()
    return redirect('/group/'+str(schedule.group_ac.id))


def check(request):
    invitations = Invite.objects.all()
    us = User_account.objects.get(name = request.user)
    invi_us = Invite()

    for invi in invitations:
        if invi.receive == us.nickname:
            invi_us = Invite.objects.get(receive = us.nickname)
            break
    return render(request, 'check.html', {'invi_us':invi_us,'us':us})


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

def map(request):
    return render(request, 'map.html')

# def delete(request,user_id):

    
