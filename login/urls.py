from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'login'
urlpatterns = [
    path('loginp/', views.loginp, name='loginp'),
    path('logout/', views.logout, name='logout'),
    path('loginID/', views.loginID, name='loginID'),
    path('loginPW/', views.loginPW, name='loginPW'),
    path('loginCPW/', views.loginCPW, name='loginCPW'),
    path('send_code/', views.send_verification_code, name='send_code'),
    
  # 카카오로그인
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/oauth/', views.kakao_callback, name='kakao_oauth'), 
]