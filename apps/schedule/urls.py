from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("main/", views.main, name="main"),
    path("calender/", views.calender_view, name="calender"),
    path("reservation/", views.reservation, name="reservation"),
    path("sent/", views.sent, name="sent"),
    path('month/', views.MonthCalendar.as_view(), name='month'),
    path('month/<int:year>/<int:month>/', views.MonthCalendar.as_view(), name='month'),
]
