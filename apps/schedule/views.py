from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Group
from django.views import generic
import calendar
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView
from .forms import UserCreateForm, ScheduleForm, ScheduleCondition
from .models import UserName, ScheduleCondition
from django.views import View

#render テンプレートをロードし、コンテキストに値を入れる。
#コンテキストはテンプレート内の辺薄をpythonオブジェクトにマップする辞書。

#トップページ
def index(request):
    template = loader.get_template("schedule/index.html")
    context = {
    }
    return HttpResponse(template.render(context, request))

#トップページからカレンダーページへ推移(トップページのボタンで推移)
def go_to_calender(request):
    username = ""
    #ユーザー名を取得して、予約画面の表示を分岐させる。
    if request.method == 'GET':
        username = request.GET.get("username")
    template = loader.get_template("schedule/calender.html")
    month = datetime.now().month
    #9〜24時の間で予約させる
    time = [n for n in range(9, 25)]
    place = ""
    #今月の月数を取得
    month_days = calendar.monthrange(2021, month)[1]
    #月数をリスト化
    month_days = [i for i in range(1, (month_days+1))]
    calendar_list = []
    start_time = 0
    end_time = 0
    delta = 0
    time_search_list = []
    data_time = ""
    data_place = []

    #POSTリクエスト時の処理
    if request.method == "POST":
        #場所検索処理
        if request.POST.get("place") == "0":
            place = "梅田"
        elif request.POST.get("place") == "1":
            place = "難波"
        elif request.POST.get("place") == "2":
            place = "岸和田"
        elif request.POST.get("place") == "3":
            place = "布施"
        elif request.POST.get("place") == "4":
            place = "梅田or難波"
        else:
            place = "未定"

        #時間検索処理
        start = int(request.POST.get("start_time"))
        end = int(request.POST.get("end_time"))
        start_time = datetime(2021, month, 1, start, 0, 0)
        end_time = datetime(2021, month, 1, end, 0, 0)
        start_time_all = datetime(2021, month, 1, 9, 0, 0)
        end_time_all = datetime(2021, month, 1, 23, 0, 0)
        delta = int((end - start) / 0.5)

        if start != 0 and end != 0:
            time_search_list = ["{:02d}:{:02d}-{:02d}:{:02d}".format((start_time + timedelta(minutes=n * 30)).hour,
                            (start_time + timedelta(minutes=n * 30)).minute,
                            (start_time + timedelta(minutes=(n + 1) * 30)).hour,
                            (start_time + timedelta(minutes=(n + 1) * 30)).minute) for n in range(0, delta)]
        else:
            time_search_list = ["{:02d}:{:02d}-{:02d}:{:02d}".format((start_time_all + timedelta(minutes=n * 30)).hour,
                             (start_time_all + timedelta(minutes=n * 30)).minute,
                             (start_time_all + timedelta(minutes=(n + 1) * 30)).hour,
                             (start_time_all + timedelta(minutes=(n + 1) * 30)).minute) for n in range(0, int((24-9)/0.5))]

        #月の各日に検索をかける
        for i in month_days:
            data = ScheduleCondition.objects.filter(month=month, day=i, day_condition="空き", place=place)
            data_time = list(data.values_list("time", flat=True))
            #１時間以上空きがあれば、空いている状態にする。
            try:
                dummy = data_time[1]
                for n in time_search_list:
                    if n in data_time:
                        data_place.append(1)
                if data_place.count(1) > 1:
                    calendar_list.append("place")
                else:
                    calendar_list.append("no_place")
            except:
                calendar_list.append("no_place")

    else:
        calendar_list = month_days

    context = {
        "month": month,
        "time": time,
        "month_days": month_days,
        "calendar_list": calendar_list,
        "username": username,
    }
    return HttpResponse(template.render(context, request))

#予約画面へ推移(カレンダーの日にちボタンから)
def calender_view(request):
    #取得したユーザー名で表示を分岐させる
    username = ""
    if request.method == 'GET':
        username = request.GET.get("username")
    #ホスト用
    if username == "yusuke":
        template = loader.get_template("schedule/reservation_host.html")
    #ゲスト用
    else:
        template = loader.get_template("schedule/reservation.html")
    day = ""
    month = datetime.now().month
    #9時から予約可能
    start = 9
    start_time = datetime(2021, 1, 1, start, 0, 0)
    #月の日数のみ取得
    month_days = calendar.monthrange(2021, month)[1]
    #日にちボタンの日にちを取得
    if request.method == 'GET':
        day = request.GET.get("day")
    else:
        day = "error"

    #データベースから月と日にちが合致するデータを取得
    data = ScheduleCondition.objects.filter(day=day, month=month)
    if len(data) == 0:
        data = [n for n in range(1, (month_days+1))]
    data_1 = data[1:7]
    data_2 = data[7:13]
    data_3 = data[13:19]
    data_4 = data[19:25]
    data_5 = data[25:(month_days)]

    context = {
        "username": username,
        "day": day,
        "month": month,
        'condition_1': [str(n) for n in range(1, 7)],
        'condition_2': [str(n) for n in range(7, 13)],
        'condition_3': [str(n) for n in range(13, 19)],
        'condition_4': [str(n) for n in range(19, 25)],
        'condition_5': [str(n) for n in range(25, (month_days+1))],
        'place_1': ["place_"+str(n) for n in range(1, 7)],
        'place_2': ["place_"+str(n) for n in range(7, 13)],
        'place_3': ["place_"+str(n) for n in range(13, 19)],
        'place_4': ["place_"+str(n) for n in range(19, 25)],
        'place_5': ["place_"+str(n) for n in range(25, (month_days+1))],
        'time_1': ["{:02d}:{:02d}-{:02d}:{:02d}".format((start_time + timedelta(minutes=n * 30)).hour,
                                                        (start_time + timedelta(minutes=n * 30)).minute,
                                                        (start_time + timedelta(minutes=(n + 1) * 30)).hour,
                                                        (start_time + timedelta(minutes=(n + 1) * 30)).minute) for n in range(0, 6)],
        'time_2': ["{:02d}:{:02d}-{:02d}:{:02d}".format((start_time + timedelta(minutes=n * 30)).hour,
                                                        (start_time + timedelta(minutes=n * 30)).minute,
                                                        (start_time + timedelta(minutes=(n + 1) * 30)).hour,
                                                        (start_time + timedelta(minutes=(n + 1) * 30)).minute) for n in range(6, 12)],
        'time_3': ["{:02d}:{:02d}-{:02d}:{:02d}".format((start_time + timedelta(minutes=n * 30)).hour,
                                                        (start_time + timedelta(minutes=n * 30)).minute,
                                                        (start_time + timedelta(minutes=(n + 1) * 30)).hour,
                                                        (start_time + timedelta(minutes=(n + 1) * 30)).minute) for n in range(12, 18)],
        'time_4': ["{:02d}:{:02d}-{:02d}:{:02d}".format((start_time + timedelta(minutes=n * 30)).hour,
                                                        (start_time + timedelta(minutes=n * 30)).minute,
                                                        (start_time + timedelta(minutes=(n + 1) * 30)).hour,
                                                        (start_time + timedelta(minutes=(n + 1) * 30)).minute) for n in range(18, 24)],
        'time_5': ["{:02d}:{:02d}-{:02d}:{:02d}".format((start_time + timedelta(minutes=n * 30)).hour,
                                                        (start_time + timedelta(minutes=n * 30)).minute,
                                                        (start_time + timedelta(minutes=(n + 1) * 30)).hour,
                                                        (start_time + timedelta(minutes=(n + 1) * 30)).minute) for n in range(24, 30)],

        "data_1": data_1,
        "data_2": data_2,
        "data_3": data_3,
        "data_4": data_4,
        "data_5": data_5,
    }
    return HttpResponse(template.render(context, request))

def reservation(request):
    username = ""
    month = datetime.now().month
    day = ""
    start = 9
    start_time = datetime(2021, 1, 1, start, 0, 0)
    current_time = datetime.now()
    template = loader.get_template("schedule/sent.html")
    schedule_form = ScheduleForm()
    time_reserve = []
    month_days = calendar.monthrange(2021, month)[1]

    context = {
        "current_time": current_time,
        "scheduleForm": schedule_form,
        "month": month,
    }

    if request.method == 'POST':
        username = request.POST.get("username")
        if request.POST.get("pass") == "siluro":
            day = request.POST.get("day")
            context["day"] = day
            scheduleForm = ScheduleForm(request.POST)
            if scheduleForm.is_valid():
                scheduleForm.save()

            for i in range(1, month_days):
                if request.POST.get(i) == "0":
                    selected_i = "予約不可"
                elif request.POST.get(i) == "1":
                    selected_i = "予約申請する"
                else:
                    selected_i = "空き"

                time_i = "{:02d}:{:02d}-{:02d}:{:02d}".format((start_time + timedelta(minutes=(i - 1) * 30)).hour,
                                                              (start_time + timedelta(minutes=(i - 1) * 30)).minute,
                                                              (start_time + timedelta(minutes=i * 30)).hour,
                                                              (start_time + timedelta(minutes=i * 30)).minute)

                if selected_i == "予約申請する":
                    time_reserve.append(time_i)
                Sc = ScheduleCondition(month=month, day=day, day_condition=selected_i, user_name=username, time=time_i)
                Sc.save()
                context[str(selected_i)] = selected_i
        context["time_reserve_first"] = time_reserve[0][:5]
        context["time_reserve_last"] = time_reserve[-1][-5:]

    return HttpResponse(template.render(context, request))

def reservation_host(request):
    username = ""
    current_time = datetime.now()
    start = 9
    start_time = datetime(2021, 1, 1, start, 0, 0)
    template = loader.get_template("schedule/sent.html")
    schedule_form = ScheduleForm()
    selected = []
    place = []
    time = []
    day = ""
    month = datetime.now().month
    place_reserve = []
    time_reserve = []
    month_days = calendar.monthrange(2021, month)[1]

    if request.method == 'POST':
        username = request.POST.get("username")
        if request.POST.get("pass") == "siluro":
            scheduleForm = ScheduleForm(request.POST)
            if scheduleForm.is_valid():
                scheduleForm.save()

            for i in range(1, (month_days+1)):
                if request.POST.get(str(i)) == "0":
                    selected_i = "予約不可"
                elif request.POST.get(str(i)) == "1":
                    selected_i = "予約申請する"
                else:
                    selected_i = "空き"

                if request.POST.get("place_"+str(i)) == "0":
                    place_i = "梅田"
                elif request.POST.get("place_"+str(i)) == "1":
                    place_i = "難波"
                elif request.POST.get("place_"+str(i)) == "2":
                    place_i = "岸和田"
                elif request.POST.get("place_"+str(i)) == "3":
                    place_i = "布施"
                elif request.POST.get("place_"+str(i)) == "4":
                    place_i = "梅田or難波"
                else:
                    place_i = "未定"

                time_i = "{:02d}:{:02d}-{:02d}:{:02d}".format((start_time + timedelta(minutes=(i-1) * 30)).hour,
                                                              (start_time + timedelta(minutes=(i-1) * 30)).minute,
                                                              (start_time + timedelta(minutes=i * 30)).hour,
                                                              (start_time + timedelta(minutes=i * 30)).minute)
                month = request.POST.get("month")
                day = request.POST.get("day")

                if selected_i == "予約申請する":
                    place_reserve.append(place_i)
                    time_reserve.append(time_i)

                Sc = ScheduleCondition(month=month, day=day, day_condition=selected_i, place=place_i, time=time_i,
                                       user_name=username)
                Sc.save()

                selected.append(selected_i)
                place.append(place_i)
                time.append(time_i)
        else:
            context = {}
            template = loader.get_template("schedule/error.html")
            return HttpResponse(template.render(context, request))

    context = {
        "day": day,
        "month": month,
        "current_time": current_time,
        "scheduleForm": schedule_form,
        "selected": selected,
        "place": place,
        "time": time,
        "place_reserve": place_reserve[0],
        "time_reserve_first": time_reserve[0][:5],
        "time_reserve_last": time_reserve[-1][-5:],
        "month_days": month_days,
    }

    return HttpResponse(template.render(context, request))

def sent(request):
    template = loader.get_template("schedule/sent.html")
    current_time = datetime.now()

    context = {
        "current_time": current_time,
    }
    return HttpResponse(template.render(context, request))

class Create_account(CreateView):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            #フォームから'username'を読み取る
            username = form.cleaned_data.get('username')
            #フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        return render(request, 'create.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return  render(request, 'create.html', {'form': form,})

create_account = Create_account.as_view()


class Account_login(View):
    def post(self, request, *arg, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('/')
        return render(request, 'login.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        return render(request, 'login.html', {'form': form,})

account_login = Account_login.as_view()