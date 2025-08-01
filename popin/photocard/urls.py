from django.urls import path, include
from . import views

app_name = 'photocard'

urlpatterns = [
    path('list/', views.list, name='list'),
    path('view/<int:pno>/', views.view, name='view'),
    path('exchange/', views.exchange, name='exchange'),
    path('detail/<int:pno>/', views.detail, name='detail'),
    path('write/', views.write, name='write'),
    path('update/<int:pno>/', views.update, name='update'),
    path('delete/<int:pno>/', views.delete, name='delete'),
    path('wish/<int:pno>/', views.wish, name='wish'),
    path('toggle_wish/<int:pno>/', views.toggle_wish, name='toggle_wish'),
    path('modify/<int:pno>/', views.modify, name='modify'),
    path('location/', views.location, name='location'),
    
    path('search_poca/',views.search_poca,name='search_poca'), # 타인 프로필
    path('marker_detail/<int:pno>/', views.marker_detail, name='marker_detail'),
]
