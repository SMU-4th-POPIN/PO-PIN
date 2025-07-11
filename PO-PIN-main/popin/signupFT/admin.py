from django.contrib import admin
from .models import User,UserRelation # 정의한 모델들을 임포트합니다.

# UserRelation 모델을 관리자 페이지에 등록
admin.site.register(UserRelation)


# User 모델을 관리자 페이지에 등록
admin.site.register(User)

