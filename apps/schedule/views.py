from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Group
from django.views import generic
from . import calender
import datetime
from django.contrib.auth.models import User
from .forms import UserForm, ScheduleForm
from .models import UserName

#render テンプレートをロードし、コンテキストに値を入れる。
#コンテキストはテンプレート内の辺薄をpythonオブジェクトにマップする辞書。


def index(request):
    template = loader.get_template("schedule/index.html")
    context = {
        "test":"abc",
    }
    return HttpResponse(template.render(context, request))


def calender_view(request):
    template = loader.get_template("schedule/calender.html")
    context = {
        "test": "zzz",
    }
    return HttpResponse(template.render(context, request))

def reservation(request):
    template = loader.get_template("schedule/reservation.html")
    form = UserForm()
    schedule_form = ScheduleForm()

    if request.method == 'POST':
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            userForm.save()

    if request.method == 'POST':
        scheduleForm = ScheduleForm(request.POST)
        if scheduleForm.is_valid():
            scheduleForm.save()

    current_time = datetime.datetime.now()
    context = {
        "current_time": current_time,
        "userForm": form,
        "scheduleForm": schedule_form,
    }
    return HttpResponse(template.render(context, request))

def sent(request):
    template = loader.get_template("schedule/sent.html")
    current_time = datetime.datetime.now()
    context = {
        "current_time": current_time,
    }
    return HttpResponse(template.render(context, request))

"""

def sign_up(request):
    template = loader.get_template("allauth/account/signup.html")
    #if request.method == 'POST':
     #   form = SignUpForm(request.POST)
      #  if form.is_valid():
       #     form.save()
        #    return redirect('schedule/templates/index.html')
    #else:
     #   form = SignUpForm()

    context = {"test": "zzz"}#{'form':form}
    return HttpResponse(template.render(context, request))#render(request, 'schedule/templates/sign_up.html', context)


def login(request):
    template = loader.get_template("allauth/account/login.html")
    #if request.method == 'POST':
     #   form = SignUpForm(request.POST)
      #  if form.is_valid():
       #     form.save()
        #    return redirect('schedule/templates/index.html')
    #else:
     #   form = SignUpForm()

    context = {"test": "zzz"}#{'form':form}
    return HttpResponse(template.render(context, request))
#"http://localhost:8000/accounts/login/"

def logout(request):
    template = loader.get_template("allauth/account/logout.html")
    #if request.method == 'POST':
     #   form = SignUpForm(request.POST)
      #  if form.is_valid():
       #     form.save()
        #    return redirect('schedule/templates/index.html')
    #else:
     #   form = SignUpForm()

    context = {"test": "zzz"}#{'form':form}
    return HttpResponse(template.render(context, request))



"""


def addUser(request):
    if request.method == 'POST':
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            userForm.save()
    if request.method == 'POST':
        scheduleForm = ScheduleForm(request.POST)
        if scheduleForm.is_valid():
            scheduleForm.save()

    # 登録後、全件データを抽出
    """
    user_name = UserName.objects.all()
    context = {
        'msg': '現在の利用状況',
        'userinfo': user_name,
        'count': user_name.count,
    }
    print("TEST",user_name)
    """
    context = {
        'count': "aa"
    }

    # user.htmlへデータを渡す
    return render(request, 'schedule/reservation.html', context)