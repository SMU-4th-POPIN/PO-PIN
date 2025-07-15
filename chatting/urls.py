from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'change'
urlpatterns = [
    path('', views.signupFT, name='signupFT'),
]
