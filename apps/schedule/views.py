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
from django.views import View

#render テンプレートをロードし、コンテキストに値を入れる。
#コンテキストはテンプレート内の辺薄をpythonオブジェクトにマップする辞書。

class Schedule(View):


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

        if request.POST["day1"] == "0":
            selected_1 = "予約不可"
        elif request.POST["day1"] == "1":
            selected_1 = "予約申請する"
        else:
            selected_1 = "空き"


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

shedule_func = Schedule.as_view()

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