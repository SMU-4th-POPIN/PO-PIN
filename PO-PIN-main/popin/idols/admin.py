from django.contrib import admin
from .models import Group, Member

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'gender', 'debut_date')
    search_fields = ('name', 'code')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'birth_date')
    list_filter = ('group',) # 그룹별 필터링
    search_fields = ('name',)