from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("main/", views.main, name="main"),
    path('month/', views.MonthCalendar.as_view(), name='month'),
    path('month/<int:year>/<int:month>/', views.MonthCalendar.as_view(), name='month'),
]
