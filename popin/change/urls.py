from django.urls import path
from . import views

urlpatterns = [
    path('chatting/', views.chatting_page, name='chatting'),  
]