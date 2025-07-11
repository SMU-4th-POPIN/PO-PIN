from django.db import models

class Group(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="그룹 코드")
    name = models.CharField(max_length=100, unique=True, verbose_name="그룹명")
    name_en = models.CharField(max_length=100, verbose_name="그룹영어명", default="")
    
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
        ('U', '혼성/알 수 없음'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name="그룹 성별")
    debut_date = models.DateField(blank=True, null=True, verbose_name="데뷔일")
    # 기타 필요한 그룹 정보 필드 추가 가능
    class Meta:
        verbose_name = "아이돌 그룹"
        verbose_name_plural = "아이돌 그룹 목록"
        ordering = ['name'] # 그룹명을 기준으로 정렬

    def __str__(self):
        return f"{self.name}/{self.name_en}" # 관리자 페이지 등에서 그룹 이름으로 표시

class Member(models.Model):
    # 멤버의 고유 식별자로 사용할 코드 (선택 사항, 필요하다면)
    # code = models.CharField(max_length=50, unique=True, verbose_name="멤버 코드")
    
    # 멤버의 실제 이름 (사용자에게 보여줄 이름)
    name = models.CharField(max_length=100, verbose_name="멤버 이름")
    name_en = models.CharField(max_length=100, verbose_name="멤버 영어이름",default="")
    
    # 이 멤버가 속한 그룹 (Group 모델과 N:1 관계)
    # 그룹이 삭제되면 멤버도 삭제되도록 CASCADE 설정
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members', verbose_name="소속 그룹")
    
    # 멤버의 생년월일 (선택 사항)
    birth_date = models.DateField(blank=True, null=True, verbose_name="생년월일")
    
    # 기타 필요한 멤버 정보 필드 추가 가능

    class Meta:
        verbose_name = "아이돌 멤버"
        verbose_name_plural = "아이돌 멤버 목록"
        # 한 그룹 내에서 멤버 이름은 유니크해야 할 가능성이 높습니다.
        unique_together = ('group', 'name') 
        ordering = ['group__name', 'name'] # 그룹명, 멤버명 순으로 정렬

    def __str__(self):
        return f"{self.group.name} - {self.name}" # 관리자 페이지 등에서 "그룹명 - 멤버명"으로 표시