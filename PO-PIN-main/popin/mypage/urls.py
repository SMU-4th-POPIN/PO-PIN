from django.urls import path, include
from.import views

app_name = 'mypage'
urlpatterns = [
    path('profile/',views.profile,name='profile'),
    path('keyword/', views.keyword, name='keyword'),
    path('test/', views.test, name='test'),
    path('mypoca/', views.my_poca, name='my_poca'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('trade/', views.trade, name='trade'),
    path('latest/', views.latest_post, name='latest_post'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('blocklist/', views.block_list, name='block_list'),
    path('update_blocklist/', views.update_blocklist, name='update_blocklist'),
    
]
