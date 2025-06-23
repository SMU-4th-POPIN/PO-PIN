from django.contrib import admin
from .models import User, UserPreference, UserRelation # 정의한 모델들을 임포트합니다.

# User 모델을 관리자 페이지에 등록
admin.site.register(User)

# UserPreference 모델을 관리자 페이지에 등록
admin.site.register(UserPreference)

# UserRelation 모델을 관리자 페이지에 등록
admin.site.register(UserRelation)