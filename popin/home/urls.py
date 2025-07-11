from django.urls import path, include
from . import views

app_name = 'home'
urlpatterns = [
    path('main/', views.main, name='main'),
    path('recent/', views.recent, name='recent'),
]
