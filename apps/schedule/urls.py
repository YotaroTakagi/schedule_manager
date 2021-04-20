from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("calender/", views.calender_view, name="calender"),
    path("reservation/", views.reservation, name="reservation"),
    path("sent/", views.sent, name="sent"),
    #path("reservation/", views.addUser, name="add"),
    #path("sign_up/", views.sign_up, name="sign_up"),
    #path("login/", views.login, name="login"),
    #path("logout/", views.logout, name="logout"),
    #path('accounts/login/', auth_views.LoginView.as_view(template_name="schedule/login.html"), name='login'),
    #path('accounts/profile/', auth_views.LogoutView.as_view(next_page="schedule/index"), name='logout'),

]
