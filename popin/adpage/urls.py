from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'adpage'
urlpatterns = [
    path('', views.main, name='main'),                      # 관리자 대시보드
    path('user/', views.user, name='user'),                 # 사용자관리
    path('user/delete/', views.delete_user, name='delete_user'),  # 계정 삭제
    path('user/block/', views.block_user, name='block_user'),      # 계정 정지 / 정지 해제
    path('post/', views.post, name='post'),                 # 게시글관리
    path('postV/', views.postV, name='postV'),              # 게시글상세보기
    path('notice/', views.notice, name='notice'),           # 공지사항 목록
    path('noticeW/', views.noticeW, name='noticeW'),        # 공지사항 작성
    path('noticeV/<int:notice_id>/', views.noticeV, name='noticeV'),        # 공지사항 상세보기
    path('noticeR/<int:notice_id>/', views.noticeR, name='noticeR'),        # 공지사항 수정
    path('noticeD/<int:notice_id>/', views.noticeD, name='noticeD'),        # 공지사항 삭제
]