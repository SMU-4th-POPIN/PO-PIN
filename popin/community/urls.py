from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('chgReview/main/', views.chgReviewmain, name='chgReviewmain'),
    path('chgReview/view/<int:pk>/', views.chgReviewview, name='chgReviewview'),
   
    path('recent/', views.recent, name='recent'),
    path('write/companion/', views.write_companion, name='write_companion'),
    path('write/proxy/', views.write_proxy, name='write_proxy'),
    path('write/review/', views.write_review, name='write_review'),
    path('write/sharing/', views.write_sharing, name='write_sharing'),
    path('write/status/', views.write_status, name='write_status'),


    path('', views.main, name='main'),

    path('companion/', views.companion, name='companion'),
    path('proxy/', views.proxy, name='proxy'),
    path('sharing/', views.sharing, name='sharing'),
    path('status/', views.status, name='status'),
    # 수정
    path("updateC/<int:pk>/", views.updateC, name="updateC"),
    path('updateCo/<int:pk>/', views.updateCo, name='updateCo'),
    path('updateP/<int:pk>/', views.updateP, name='updateP'),
    path('updateSh/<int:pk>/', views.updateSh, name='updateSh'),
    path('updateS/<int:pk>/', views.updateS, name='updateS'),
    # 상세페이지 
    path('companion/<int:pk>/', views.companionview, name='companionview'),
    path('proxy/<int:pk>/', views.proxyview, name='proxyview'),
    path('sharing/<int:pk>/', views.sharingview, name='sharingview'),
    path('status/<int:pk>/', views.statusview, name='statusview'),
    
    path('mypage_community_list/', views.mypage_community_list, name='mypage_community_list'),
    #신고버튼누르면카운트db저장
    path('report_post/<str:post_type>/<int:post_id>/', views.report_post, name='report_post'),
    #  차단/해제 토글 API
    path('block/companion/<int:post_id>/', views.toggle_block_companion, name='toggle_block_companion'),
    path('block/sharing/<int:post_id>/', views.toggle_block_sharing, name='toggle_block_sharing'),
    path('block/proxy/<int:post_id>/', views.toggle_block_proxy, name='toggle_block_proxy'),
    path('block/status/<int:post_id>/', views.toggle_block_status, name='toggle_block_status'),
    path('block/review/<int:post_id>/', views.toggle_block_review, name='toggle_block_review'),

    #  마이페이지 차단목록 조회 API
    path('mypage/blocked/api/', views.mypage_blocked_list_api, name='mypage_blocked_api'),


]