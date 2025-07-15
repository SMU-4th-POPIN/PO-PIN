from django.urls import path, include
from . import views

app_name = 'customer'
urlpatterns = [
    path('information/', views.information, name='information'),
    path('notice/', views.notice, name='notice'),
    path('notice_view/<int:id>/', views.notice_view, name='notice_view'),
    path('qna/', views.QnA, name='QnA'),
    path('filter_notice/', views.filter_notice, name='filter_notice'),
]
