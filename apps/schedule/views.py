from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Group

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