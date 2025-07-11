
from django.urls import path
from . import views

app_name = 'pocadeco'

urlpatterns = [
    path('main/', views.main, name='main'), 
    path('mydecolist/', views.mydecolist, name='mydecolist'), 
]