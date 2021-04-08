from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Group
from django.views import generic
from . import calender
import datetime

#render テンプレートをロードし、コンテキストに値を入れる。
#コンテキストはテンプレート内の辺薄をpythonオブジェクトにマップする辞書。


def index(request):
    template = loader.get_template("schedule/index.html")
    context = {
        "test":"abc",
    }
    return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template("schedule/main.html")
    context = {
        "test": "zzz",
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
    current_time = datetime.datetime.now()
    context = {
        "current_time": current_time,
    }
    return HttpResponse(template.render(context, request))

def sent(request):
    template = loader.get_template("schedule/sent.html")
    current_time = datetime.datetime.now()
    context = {
        "current_time": current_time,
    }
    return HttpResponse(template.render(context, request))


class MonthCalendar(calender.Calender, generic.TemplateView):
    """月間カレンダーを表示するビュー"""
    template_name = 'schedule/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

