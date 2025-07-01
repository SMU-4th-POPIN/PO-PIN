from django.urls import path, include
from.import views

app_name = 'mypage'
urlpatterns = [
    path('mypage/',views.mypage,name='mypage'),
    path('pchange/',views.pchange,name='pchange'),
    path('showMybiasModal/',views.showMybiasModal,name='showMybiasModal'),
]
