from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
#from django.contrib.auth.views import logout

urlpatterns = [
    path("", views.index, name="index"),
    path("calender/view/", views.go_to_calender, name="go_to_calender"),
    path("calender/", views.calender_view, name="calender"),
    path("reservation/", views.reservation, name="reservation"),
    path("reservation_host/", views.reservation_host, name="reservation_host"),
    path("sent/", views.sent, name="sent"),

    #path("create_account/", views.Create_account, name="create_account"),
    #path("login/", views.Account_login, name="login"),
    #path(r'^logout/$', logout, {'template_name': 'index.html'}, name='logout'),
    #path('accounts/login/', auth_views.LoginView.as_view(template_name="schedule/login.html"), name='login'),
    #path('accounts/profile/', auth_views.LogoutView.as_view(next_page="schedule/index"), name='logout'),

]
