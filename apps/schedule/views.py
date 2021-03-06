import calendar
from django.http import HttpResponse
from django.template import loader
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from .forms import ScheduleForm, ScheduleCondition
from .models import ScheduleCondition
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#render テンプレートをロードし、コンテキストに値を入れる。
#コンテキストはテンプレート内の辺薄をpythonオブジェクトにマップする辞書。

#ページネーション
def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

    ページングしたい場合に利用してください。

    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。

        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}

    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

#トップページ
def index(request):
    template = loader.get_template("schedule/index.html")
    context = {
    }
    return HttpResponse(template.render(context, request))

#トップページからカレンダーページへ推移(トップページのボタンで推移)
def go_to_calender(request):
    username = ""
    next_bool = "0"
    today = datetime.today()
    #ユーザー名を取得して、予約画面の表示を分岐させる。
    if request.method == 'GET':
        username = request.GET.get("username")
    template = loader.get_template("schedule/calender.html")
    month = datetime.now().month
    next_month = (today + relativedelta(months=1)).month
    #9〜24時の間で予約させる
    time = [n for n in range(9, 25)]
    place = ""
    #今月の月数を取得
    month_days = calendar.monthrange(2021, month)[1]
    #次月の月数を取得
    next_month_days = calendar.monthrange(2021, next_month)[1]
    #月数をリスト化
    month_days = [i for i in range(1, (month_days+1))]
    next_month_days = [i for i in range(1, (next_month_days + 1))]
    calendar_list = []
    start_time = 0
    del_start_time = datetime(2021, 1, 1, 9, 0, 0)
    weekdays = [datetime(2021, month, n) for n in range(1, 8)]
    week_name = [n.weekday() for n in weekdays]
    week_list = []
    for i in week_name:
        if i == 0:
            week_list.append("月曜日")
        elif i == 1:
            week_list.append("火曜日")
        elif i == 2:
            week_list.append("水曜日")
        elif i == 3:
            week_list.append("木曜日")
        elif i == 4:
            week_list.append("金曜日")
        elif i == 5:
            week_list.append("土曜日")
        else:
            week_list.append("日曜日")

    data_place = []
    reservation_list = []
    reservation_list_guest = []
    delete_list = []
    del_time_list = ["{:02d}:{:02d}-{:02d}:{:02d}".format((del_start_time + timedelta(minutes=n * 30)).hour,
                                                      (del_start_time + timedelta(minutes=n * 30)).minute,
                                                      (del_start_time + timedelta(minutes=(n + 1) * 30)).hour,
                                                      (del_start_time + timedelta(minutes=(n + 1) * 30)).minute)
                                                        for n in range(0, 30)]


    #POSTリクエスト時の処理、検索処理
    if request.method == "POST":
        username = request.POST.get("username")
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
        start_time_all = datetime(2021, month, 1, 9, 0, 0)
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
            data = ScheduleCondition.objects.filter(month=month, day=i, place=place).exclude(day_condition="予約不可")
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

        reservation_data = ScheduleCondition.objects.filter(month=month, day_condition="予約不可").exclude(
                                                                user_name="yusuke").order_by("created_at")
        for i in reservation_data:
            reservation_list.append(i.user_name)
            reservation_list.append(i.month)
            reservation_list.append(i.day)
            reservation_list.append(i.time)
            reservation_list.append(i.place)
            reservation_list.append(i.day_condition)
            reservation_list.append(i.created_at)

        reservation_list = list(reservation_list)
        len_reservation_list = len(reservation_list)

        delete_data = ScheduleCondition.objects.filter(month=month, day_condition="予約取り消し済み").exclude(
                                                        user_name="yusuke").order_by("created_at")
        for i in delete_data:
            delete_list.append(i.user_name)
            delete_list.append(i.month)
            delete_list.append(i.day)
            delete_list.append(i.time)
            delete_list.append(i.place)
            delete_list.append(i.day_condition)
            delete_list.append(i.created_at)

        delete_list = list(delete_list)
        len_delete_list = len(delete_list)

        reservation_data_guest = ScheduleCondition.objects.filter(month=month, day_condition="予約不可",
                                                                  user_name=username).order_by("created_at")
        for i in reservation_data_guest:
            reservation_list_guest.append(i.user_name)
            reservation_list_guest.append(i.month)
            reservation_list_guest.append(i.day)
            reservation_list_guest.append(i.time)
            reservation_list_guest.append(i.place)
            reservation_list_guest.append(i.day_condition)
            reservation_list_guest.append(i.created_at)

        reservation_list_guest = list(reservation_list_guest)
        len_reservation_list_guest = len(reservation_list_guest)

    #GETリクエストのとき(カレンダーページに推移してきたとき、予約取り消し処理のとき)
    else:
        calendar_list = month_days

        # 予約取り消し処理
        if request.GET.get("delete") == "delete":
            print("TEST00000")
            username = request.GET.get("username")
            del_day = request.GET.get("del_day")
            del_time = request.GET.get("del_time")
            del_reservation_data = ScheduleCondition.objects.filter(month=month, user_name=username,
                                                                    day_condition="予約不可")
            del_reserve_list = list(del_reservation_data.values_list("time", flat=True))
            print("TEST")
            print(del_reserve_list)
            for i in del_reserve_list:
                if del_time == i:
                    print("UPDATE")
                    del_data = ScheduleCondition.objects.get(month=month, day=del_day, user_name=username, time=del_time,
                                                             day_condition="予約不可")
                    del_data.day_condition = "予約取り消し済み"
                    del_data.user_name = username
                    del_data.created_at = datetime.now()
                    del_data.save()
                    break

        reservation_data = ScheduleCondition.objects.filter(month=month, day_condition="予約不可").exclude(
                                                                user_name="yusuke").order_by("created_at")
        for i in reservation_data:
            reservation_list.append(i.user_name)
            reservation_list.append(i.month)
            reservation_list.append(i.day)
            reservation_list.append(i.time)
            reservation_list.append(i.place)
            reservation_list.append(i.day_condition)
            reservation_list.append(i.created_at)

        reservation_list = list(reservation_list)
        len_reservation_list = len(reservation_list)

        delete_data = ScheduleCondition.objects.filter(month=month, day_condition="予約取り消し済み").exclude(
            user_name="yusuke").order_by("created_at")
        for i in delete_data:
            delete_list.append(i.user_name)
            delete_list.append(i.month)
            delete_list.append(i.day)
            delete_list.append(i.time)
            delete_list.append(i.place)
            delete_list.append(i.day_condition)
            delete_list.append(i.created_at)

        delete_list = list(delete_list)
        len_delete_list = len(delete_list)

        reservation_data_guest = ScheduleCondition.objects.filter(month=month, day_condition="予約不可",
                                                                  user_name=username).order_by("created_at")
        for i in reservation_data_guest:
            reservation_list_guest.append(i.user_name)
            reservation_list_guest.append(i.month)
            reservation_list_guest.append(i.day)
            reservation_list_guest.append(i.time)
            reservation_list_guest.append(i.place)
            reservation_list_guest.append(i.day_condition)
            reservation_list_guest.append(i.created_at)

        reservation_list_guest = list(reservation_list_guest)
        len_reservation_list_guest = len(reservation_list_guest)

    context = {
        "month": month,
        "time": time,
        "month_days": month_days,
        "calendar_list": calendar_list,
        "username": username,
        "reservation_list": reservation_list,
        "reservation_list_guest": reservation_list_guest,
        "delete_list": delete_list,
        "len_reservation_list": len_reservation_list,
        "len_reservation_list_guest": len_reservation_list_guest,
        "len_delete_list": len_delete_list,
        "del_time_list": del_time_list,
        "next_month": next_month,
        "next_month_days": next_month_days,
        "next_bool": next_bool,
        "week_list": week_list,
    }
    return HttpResponse(template.render(context, request))

#予約画面へ推移(カレンダーの日にちボタンから)
def calender_view(request):
    #取得したユーザー名で表示を分岐させる
    username = ""
    next_bool = "0"
    if request.method == 'GET':
        username = request.GET.get("username")
        next_bool = request.GET.get("next_bool")
    #ホスト用
    if username == "yusuke":
        template = loader.get_template("schedule/reservation_host.html")
    #ゲスト用
    else:
        template = loader.get_template("schedule/reservation.html")
    today = datetime.today()
    month = datetime.now().month
    next_month = (today + relativedelta(months=1)).month
    #9時から予約可能
    start = 9
    start_time = datetime(2021, 1, 1, start, 0, 0)
    #月の日数のみ取得
    month_days = calendar.monthrange(2021, month)[1]
    next_month_days = calendar.monthrange(2021, next_month)[1]
    #日にちボタンの日にちを取得
    if request.method == 'GET':
        day = request.GET.get("day")
    else:
        day = "error"

    #データベースから月と日にちが合致するデータを取得
    data = ScheduleCondition.objects.filter(month=month, day=day)
    make_data = []
    data_len = 0
    next_data = ScheduleCondition.objects.filter(month=next_month, day=day)
    next_make_data = []
    next_data_len = 0

    if len(data) == 0:
        make_data = ["{:02d}:{:02d}-{:02d}:{:02d}".format((start_time + timedelta(minutes=n * 30)).hour,
                                          (start_time + timedelta(minutes=n * 30)).minute,
                                          (start_time + timedelta(minutes=(n + 1) * 30)).hour,
                                          (start_time + timedelta(minutes=(n + 1) * 30)).minute)
                                           for n in range(0, 30)]
        make_data = make_data[0:(month_days)]
        data = [n for n in range(0, 100)]
        data_len = len(data)
    else:
        data = data[0:30]

    if len(next_data) == 0:
        next_make_data = ["{:02d}:{:02d}-{:02d}:{:02d}".format((start_time + timedelta(minutes=n * 30)).hour,
                                          (start_time + timedelta(minutes=n * 30)).minute,
                                          (start_time + timedelta(minutes=(n + 1) * 30)).hour,
                                          (start_time + timedelta(minutes=(n + 1) * 30)).minute)
                                           for n in range(0, 30)]
        next_make_data = next_make_data[0:next_month_days]
        next_data = [n for n in range(0, 100)]
        next_data_len = len(next_data)
    else:
        next_data = next_data[0:30]

    numbers = [str(n) for n in range(1, 31)]
    numbers = numbers[0:30]
    int_numbers = [n for n in range(1, 31)]

    context = {
        "username": username,
        "day": day,
        "month": month,
        "next_month": next_month,
        'condition_1': [str(n) for n in range(1, 7)],
        'condition_2': [str(n) for n in range(7, 13)],
        'condition_3': [str(n) for n in range(13, 19)],
        'condition_4': [str(n) for n in range(19, 25)],
        'condition_5': [str(n) for n in range(25, (month_days))],
        'place_1': ["place_"+str(n) for n in range(1, 7)],
        'place_2': ["place_"+str(n) for n in range(7, 13)],
        'place_3': ["place_"+str(n) for n in range(13, 19)],
        'place_4': ["place_"+str(n) for n in range(19, 25)],
        'place_5': ["place_"+str(n) for n in range(25, (month_days))],
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
        "data": zip(numbers, data),
        "make_data": zip(numbers, make_data),
        "data_len": data_len,
        "next_data": zip(numbers, next_data),
        "next_make_data": zip(numbers, next_make_data),
        "next_data_len": next_data_len,
        "next_bool": next_bool,
    }
    return HttpResponse(template.render(context, request))

def reservation(request):
    month = datetime.now().month
    day = ""
    start = 9
    start_time = datetime(2021, 1, 1, start, 0, 0)
    current_time = datetime.now()
    template = loader.get_template("schedule/sent.html")
    schedule_form = ScheduleForm()
    time_reserve = []
    len_reserve_list = 0
    month_days = calendar.monthrange(2021, month)[1]
    update_num = 0
    today = datetime.today()
    next_month = (today + relativedelta(months=1)).month

    data = ScheduleCondition.objects.filter(day=day, month=month)
    data_time = []
    if len(data) == 0:
        data = [n for n in range(1, (month_days + 1))]
    else:
        data_time = list(data.values_list("time", flat=True))
    if len(data_time) == 0:
        data_time = [n for n in range(1, (month_days + 1))]

    context = {
        "current_time": current_time,
        "scheduleForm": schedule_form,
        "month": month,
    }

    if request.method == 'POST':
        username = request.POST.get("username")
        next_bool = request.POST.get("next_bool")
        if request.POST.get("pass") == "siluro":
            if next_bool == "0":
                day = request.POST.get("day")
                context["day"] = day
                """
                scheduleForm = ScheduleForm(request.POST)
                if scheduleForm.is_valid():
                    scheduleForm.save()
                """
                for i in range(1, 31):
                    if request.POST.get(str(i)) == "0":
                        selected_i = "予約不可"
                    elif request.POST.get(str(i)) == "1":
                        selected_i = "予約申請する"
                    else:
                        selected_i = "空き"

                    time_i = "{:02d}:{:02d}-{:02d}:{:02d}".format((start_time + timedelta(minutes=(i - 1) * 30)).hour,
                                                                  (start_time + timedelta(minutes=(i - 1) * 30)).minute,
                                                                  (start_time + timedelta(minutes=i * 30)).hour,
                                                                  (start_time + timedelta(minutes=i * 30)).minute)

                    print("TTEESSTT", request.POST.get(str(i)))
                    if selected_i == "予約申請する":
                        time_reserve.append(time_i)
                        valid = ScheduleCondition.objects.filter(month=month, day=day, time=time_i).exclude(
                                                                                     day_condition="予約不可")
                        if ScheduleCondition.objects.get(month=month, day=day, time=time_i).day_condition == "予約不可":
                            context = {"update_num": update_num, }
                            template = loader.get_template("schedule/error.html")
                            return HttpResponse(template.render(context, request))
                    else:
                        valid = None
                    #valid = len(valid)
                    #print("LEN", valid)
                    if valid is not None:
                        print("UPDATE")
                        update_num += 1
                        update = ScheduleCondition.objects.get(month=month, day=day, time=time_i)
                        update.user_name = username
                        update.day_condition = "予約不可"
                        update.created_at = datetime.now()
                        update.save()
                    else:
                        print("NO-UPDATE")
                    context[str(selected_i)] = selected_i
            #next_bool==1
            else:
                day = request.POST.get("day")
                context["day"] = day
                scheduleForm = ScheduleForm(request.POST)
                if scheduleForm.is_valid():
                    scheduleForm.save()

                for i in range(1, 31):
                    if request.POST.get(str(i)) == "0":
                        selected_i = "予約不可"
                    elif request.POST.get(str(i)) == "1":
                        selected_i = "予約申請する"
                    else:
                        selected_i = "空き"

                    time_i = "{:02d}:{:02d}-{:02d}:{:02d}".format((start_time + timedelta(minutes=(i - 1) * 30)).hour,
                                                                  (start_time + timedelta(minutes=(i - 1) * 30)).minute,
                                                                  (start_time + timedelta(minutes=i * 30)).hour,
                                                                  (start_time + timedelta(minutes=i * 30)).minute)

                    if selected_i == "予約申請する":
                        time_reserve.append(time_i)
                        valid = ScheduleCondition.objects.filter(month=next_month, day=day, time=time_i).exclude(
                            day_condition="予約不可")
                        if ScheduleCondition.objects.get(month=next_month, day=day, time=time_i).day_condition == "予約不可":
                            context = {"update_num": update_num, }
                            template = loader.get_template("schedule/error.html")
                            return HttpResponse(template.render(context, request))
                    else:
                        valid = None
                    #valid = len(valid)

                    if valid is not None:
                        print("UPDATE")
                        update_num += 1
                        update = ScheduleCondition.objects.get(month=next_month, day=day, time=time_i)
                        update.user_name = username
                        update.day_condition = "予約不可"
                        update.created_at = datetime.now()
                        update.save()
                    else:
                        print("NO-UPDATE")
                    context[str(selected_i)] = selected_i

        else:
            context = {}
            template = loader.get_template("schedule/error.html")
            return HttpResponse(template.render(context, request))

        if len(time_reserve) == 0:
            context = {}
            template = loader.get_template("schedule/error.html")
            return HttpResponse(template.render(context, request))

        context["time_reserve_first"] = time_reserve[0][:5]
        context["time_reserve_last"] = time_reserve[-1][-5:]
        context["username"] = username

        reserve_list = []
        if next_bool == "0":
            reservation_data = ScheduleCondition.objects.filter(day=day, month=month, user_name=username,
                                                                day_condition="予約不可").order_by("created_at")
        else:
            reservation_data = ScheduleCondition.objects.filter(day=day, month=next_month, user_name=username,
                                                                day_condition="予約不可").order_by("created_at")

        if reservation_data != 0:
            reserve_list = list(reservation_data.values_list("time", flat=True))
            len_reserve_list = len(reserve_list)
        context["reserve_list"] = reserve_list
        context["len_reserve_list"] = len_reserve_list
        context["reservation_data"] = reservation_data

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
    schedule_form = ScheduleForm()
    month = datetime.now().month
    place_reserve = []
    time_reserve = []
    month_days = calendar.monthrange(2021, month)[1]
    today = datetime.today()
    next_month = (today + relativedelta(months=1)).month
    next_bool = "0"

    if request.method == 'POST':
        username = request.POST.get("username")
        next_bool = request.POST.get("next_bool")
        if request.POST.get("pass") == "siluro":
            if next_bool == "0":
                scheduleForm = ScheduleForm(request.POST)
                if scheduleForm.is_valid():
                    scheduleForm.save()
                for i in range(1, 31):
                    if request.POST.get(str(i)) == "0":
                        selected_i = "予約不可"
                    else:
                        selected_i = "空き"

                    time_i = "{:02d}:{:02d}-{:02d}:{:02d}".format((start_time + timedelta(minutes=(i-1) * 30)).hour,
                                                                  (start_time + timedelta(minutes=(i-1) * 30)).minute,
                                                                  (start_time + timedelta(minutes=i * 30)).hour,
                                                                  (start_time + timedelta(minutes=i * 30)).minute)

                    if request.POST.get(time_i) == "0":
                        place_i = "梅田"
                    elif request.POST.get(time_i) == "1":
                        place_i = "難波"
                    elif request.POST.get(time_i) == "2":
                        place_i = "岸和田"
                    elif request.POST.get(time_i) == "3":
                        place_i = "布施"
                    elif request.POST.get(time_i) == "4":
                        place_i = "梅田or難波"
                    else:
                        place_i = "未定"

                    month = request.POST.get("month")
                    day = request.POST.get("day")

                    if selected_i == "空き":
                        place_reserve.append(place_i)
                        time_reserve.append(time_i)
                    else:
                        place_reserve.append("未定")
                        time_reserve.append(time_i)

                    #予約データがあるかどうか(ホスト、ゲストどちらも含む)
                    valid_host = ScheduleCondition.objects.filter(month=month, day=day, time=time_i,
                                                                  user_name=username)
                    valid_guest = ScheduleCondition.objects.filter(month=month, day=day, time=time_i).exclude(
                                                                    user_name=username)

                    if valid_host:
                        print("UPDATE")
                        update = ScheduleCondition.objects.get(month=month, day=day, time=time_i,
                                                               user_name=username)
                        update.user_name = username
                        update.day_condition = selected_i
                        update.place = place_i
                        update.created_at = datetime.now()
                        update.save()
                    elif valid_guest:
                        pass
                    else:
                        print("CREATE")
                        Sc = ScheduleCondition(month=month, day=day, day_condition=selected_i, place=place_i,
                                               time=time_i, user_name=username)
                        Sc.save()

                    selected.append(selected_i)
                    place.append(place_i)
                    time.append(time_i)
            # next_bool==1
            else:

                for i in range(1, 31):
                    if request.POST.get(str(i)) == "0":
                        selected_i = "予約不可"
                    else:
                        selected_i = "空き"

                    time_i = "{:02d}:{:02d}-{:02d}:{:02d}".format((start_time + timedelta(minutes=(i - 1) * 30)).hour,
                                                                  (start_time + timedelta(minutes=(i - 1) * 30)).minute,
                                                                  (start_time + timedelta(minutes=i * 30)).hour,
                                                                  (start_time + timedelta(minutes=i * 30)).minute)

                    if request.POST.get(time_i) == "0":
                        place_i = "梅田"
                    elif request.POST.get(time_i) == "1":
                        place_i = "難波"
                    elif request.POST.get(time_i) == "2":
                        place_i = "岸和田"
                    elif request.POST.get(time_i) == "3":
                        place_i = "布施"
                    elif request.POST.get(time_i) == "4":
                        place_i = "梅田or難波"
                    else:
                        place_i = "未定"

                    month = request.POST.get("month")
                    day = request.POST.get("day")

                    if selected_i == "空き":
                        place_reserve.append(place_i)
                        time_reserve.append(time_i)
                    else:
                        place_reserve.append("未定")
                        time_reserve.append(time_i)

                    valid = ScheduleCondition.objects.filter(month=next_month, day=day, time=time_i,
                                                             user_name=username)
                    valid = len(valid)
                    print(valid)

                    if valid != 0:
                        print("UPDATE")
                        update = ScheduleCondition.objects.get(month=next_month, day=day, time=time_i,
                                                               user_name=username)
                        update.user_name = username
                        update.day_condition = selected_i
                        update.place = place_i
                        update.created_at = datetime.now()
                        update.save()
                    else:
                        print("CREATE")
                        Sc = ScheduleCondition(month=next_month, day=day, day_condition=selected_i, place=place_i,
                                               time=time_i, user_name=username)
                        Sc.save()

                    selected.append(selected_i)
                    place.append(place_i)
                    time.append(time_i)

        else:
            context = {}
            template = loader.get_template("schedule/error.html")
            return HttpResponse(template.render(context, request))

    if next_bool == "0":
        reservation_data = ScheduleCondition.objects.filter(month=month, user_name=username,
                                                            day_condition="空き").order_by("created_at")
    else:
        reservation_data = ScheduleCondition.objects.filter(month=next_month, user_name=username,
                                                            day_condition="空き").order_by("created_at")

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
        "reservation_data": reservation_data,
    }

    return HttpResponse(template.render(context, request))

def sent(request):
    template = loader.get_template("schedule/sent.html")
    current_time = datetime.now()
    reserve_list = []
    day = ""
    month = ""
    len_reserve_list = 0
    reservation_data = None

    if request.method == 'POST':
        username = request.POST.get("username")
        month = request.POST.get("month")
        day = request.POST.get("day")
        reservation_data = ScheduleCondition.objects.filter(day=day, month=month)
        reserve_list = list(reservation_data.values_list("time", flat=True))

        if username == "yusuke":
            for i in reserve_list:
                if request.POST.get(i) == i:
                    print("UPDATE")
                    del_data = ScheduleCondition.objects.get(day=day, month=month, user_name=username,
                                                             time=i, day_condition="空き")
                    del_data.day_condition = "空き"
                    del_data.user_name = username
                    del_data.created_at = datetime.now()
                    del_data.save()
                    reservation_data = ScheduleCondition.objects.filter(month=month, user_name=username,
                                                                        day_condition="空き")
                    break
        else:
            for i in reserve_list:
                if request.POST.get(i) == i:
                    print("UPDATE")
                    del_data = ScheduleCondition.objects.get(day=day, month=month, user_name=username, time=i, day_condition="予約不可")
                    del_data.day_condition = "予約取り消し済み"
                    del_data.user_name = username
                    del_data.created_at = datetime.now()
                    del_data.save()
                    reservation_data = ScheduleCondition.objects.filter(day=day, month=month, user_name=username,
                                                                        day_condition="予約不可")
                    break

        len_reserve_list = len(reservation_data)

    context = {
        "day": day,
        "month": month,
        "reserve_list": reserve_list,
        "current_time": current_time,
        "len_reserve_list": len_reserve_list,
        "reservation_data": reservation_data,
    }
    return HttpResponse(template.render(context, request))


def go_to_next_calendar(request):
    username = ""
    next_bool = "1"
    today = datetime.today()
    #ユーザー名を取得して、予約画面の表示を分岐させる。
    if request.method == 'GET':
        username = request.GET.get("username")
    template = loader.get_template("schedule/next_calendar.html")
    month = datetime.now().month
    next_month = (today + relativedelta(months=1)).month
    #9〜24時の間で予約させる
    time = [n for n in range(9, 25)]
    #今月の月数を取得
    month_days = calendar.monthrange(2021, month)[1]
    #次月の月数を取得
    next_month_days = calendar.monthrange(2021, next_month)[1]
    #月数をリスト化
    month_days = [i for i in range(1, (month_days+1))]
    next_month_days = [i for i in range(1, (next_month_days + 1))]
    calendar_list = []
    del_start_time = datetime(2021, 1, 1, 9, 0, 0)
    weekdays = [datetime(2021, next_month, n) for n in range(1, 8)]
    week_name = [n.weekday() for n in weekdays]
    week_list = []
    for i in week_name:
        if i == 0:
            week_list.append("月曜日")
        elif i == 1:
            week_list.append("火曜日")
        elif i == 2:
            week_list.append("水曜日")
        elif i == 3:
            week_list.append("木曜日")
        elif i == 4:
            week_list.append("金曜日")
        elif i == 5:
            week_list.append("土曜日")
        else:
            week_list.append("日曜日")
    data_place = []
    reservation_list = []
    reservation_list_guest = []
    delete_list = []
    del_time_list = ["{:02d}:{:02d}-{:02d}:{:02d}".format((del_start_time + timedelta(minutes=n * 30)).hour,
                                                      (del_start_time + timedelta(minutes=n * 30)).minute,
                                                      (del_start_time + timedelta(minutes=(n + 1) * 30)).hour,
                                                      (del_start_time + timedelta(minutes=(n + 1) * 30)).minute)
                                                        for n in range(0, 30)]

    #POSTリクエスト時の処理、検索処理
    if request.method == "POST":
        username = request.POST.get("username")
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
        start_time_all = datetime(2021, month, 1, 9, 0, 0)
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
        for i in next_month_days:
            data = ScheduleCondition.objects.filter(month=next_month, day=i, place=place).exclude(day_condition="予約不可")
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

        reservation_data = ScheduleCondition.objects.filter(month=next_month, day_condition="予約不可").exclude(
                                                                user_name="yusuke").order_by("created_at")
        for i in reservation_data:
            reservation_list.append(i.user_name)
            reservation_list.append(i.month)
            reservation_list.append(i.day)
            reservation_list.append(i.time)
            reservation_list.append(i.place)
            reservation_list.append(i.day_condition)
            reservation_list.append(i.created_at)

        reservation_list = list(reservation_list)
        len_reservation_list = len(reservation_list)

        delete_data = ScheduleCondition.objects.filter(month=next_month, day_condition="予約取り消し済み").exclude(
                                                        user_name="yusuke").order_by("created_at")
        for i in delete_data:
            delete_list.append(i.user_name)
            delete_list.append(i.month)
            delete_list.append(i.day)
            delete_list.append(i.time)
            delete_list.append(i.place)
            delete_list.append(i.day_condition)
            delete_list.append(i.created_at)

        delete_list = list(delete_list)
        len_delete_list = len(delete_list)

        reservation_data_guest = ScheduleCondition.objects.filter(month=next_month, day_condition="予約不可",
                                                                  user_name=username).order_by("created_at")
        for i in reservation_data_guest:
            reservation_list_guest.append(i.user_name)
            reservation_list_guest.append(i.month)
            reservation_list_guest.append(i.day)
            reservation_list_guest.append(i.time)
            reservation_list_guest.append(i.place)
            reservation_list_guest.append(i.day_condition)
            reservation_list_guest.append(i.created_at)

        reservation_list_guest = list(reservation_list_guest)
        len_reservation_list_guest = len(reservation_list_guest)

    #GETリクエストのとき(カレンダーページに推移してきたとき、予約取り消し処理のとき)
    else:
        calendar_list = next_month_days

        # 予約取り消し処理
        if request.GET.get("delete") == "delete":
            username = request.GET.get("username")
            del_day = request.GET.get("del_day")
            del_time = request.GET.get("del_time")
            del_reservation_data = ScheduleCondition.objects.filter(month=next_month, user_name=username,
                                                                    day_condition="予約不可")
            del_reserve_list = list(del_reservation_data.values_list("time", flat=True))
            print("TEST")
            print(del_reserve_list)
            for i in del_reserve_list:
                if del_time == i:
                    print("UPDATE")
                    del_data = ScheduleCondition.objects.get(month=next_month, day=del_day, user_name=username, time=del_time,
                                                             day_condition="予約不可")
                    del_data.day_condition = "予約取り消し済み"
                    del_data.user_name = username
                    del_data.created_at = datetime.now()
                    del_data.save()
                    break

        reservation_data = ScheduleCondition.objects.filter(month=next_month, day_condition="予約不可").exclude(
                                                                user_name="yusuke").order_by("created_at")
        for i in reservation_data:
            reservation_list.append(i.user_name)
            reservation_list.append(i.month)
            reservation_list.append(i.day)
            reservation_list.append(i.time)
            reservation_list.append(i.place)
            reservation_list.append(i.day_condition)
            reservation_list.append(i.created_at)

        reservation_list = list(reservation_list)
        #reservation_data_page = paginate_queryset(request, reservation_list, 2)
        len_reservation_list = len(reservation_list)

        delete_data = ScheduleCondition.objects.filter(month=next_month, day_condition="予約取り消し済み").exclude(
            user_name="yusuke").order_by("created_at")
        for i in delete_data:
            delete_list.append(i.user_name)
            delete_list.append(i.month)
            delete_list.append(i.day)
            delete_list.append(i.time)
            delete_list.append(i.place)
            delete_list.append(i.day_condition)
            delete_list.append(i.created_at)

        delete_list = list(delete_list)
        len_delete_list = len(delete_list)

        reservation_data_guest = ScheduleCondition.objects.filter(month=next_month, day_condition="予約不可",
                                                                  user_name=username).order_by("created_at")
        for i in reservation_data_guest:
            reservation_list_guest.append(i.user_name)
            reservation_list_guest.append(i.month)
            reservation_list_guest.append(i.day)
            reservation_list_guest.append(i.time)
            reservation_list_guest.append(i.place)
            reservation_list_guest.append(i.day_condition)
            reservation_list_guest.append(i.created_at)

        reservation_list_guest = list(reservation_list_guest)
        len_reservation_list_guest = len(reservation_list_guest)


    context = {
        "month": month,
        "time": time,
        "month_days": month_days,
        "calendar_list": calendar_list,
        "username": username,
        "reservation_list": reservation_list,
        "reservation_list_guest": reservation_list_guest,
        "delete_list": delete_list,
        "len_reservation_list": len_reservation_list,
        "len_reservation_list_guest": len_reservation_list_guest,
        "len_delete_list": len_delete_list,
        "del_time_list": del_time_list,
        "next_month": next_month,
        "next_month_days": next_month_days,
        "next_bool": next_bool,
        "week_list": week_list,
    }
    return HttpResponse(template.render(context, request))