from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'myapp'

urlpatterns = [
	path('details', views.details, name='details'),
    path('', views.login , name='login'),
    path('login', views.login , name='login'),
    path('logout/', views.logout , name='logout'),
    path('billing', views.billing , name='billing'),
    path('new_billing', views.new_billing , name='new_billing'),
    path('welcome', views.welcome , name='welcome'),
    path('payment', views.payment , name='payment'),
    path('check',  views.check , name='check'),
    path('check',  views.check , name='check'),
    path('daily', views.daily , name='daily'),
    path('print_bill', views.print_bill , name='print_bill'),
    path('school_report', views.school_report , name='school_report'),
]