from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# 새로 생성한 'idols' 앱의 모델을 임포트합니다.
from idols.models import Group, Member 

# --- 기존 CHOICES 정의 (GENDER_CHOICES, USER_STATE_CHOICES는 그대로 유지) ---

GENDER_CHOICES = [
    ('M', '남성'),
    ('F', '여성'),
]

USER_STATE_CHOICES = [
    (0, '관리자'),
    (1, '일반 사용자'),
    (2, '신고된 사용자'),
    (3, '정지된 사용자'),
]
# --- CHOICES 정의 끝 ---


class User(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True, verbose_name="사용자 ID")
    password = models.CharField(max_length=255, verbose_name="비밀번호")
    name = models.CharField(max_length=100, verbose_name="이름")
    birth_date = models.DateField(null=True, blank=True ,verbose_name="생년월일")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="성별")
    email = models.EmailField(unique=True, verbose_name="이메일")
    
    # bias_group 필드를 Group 모델을 참조하는 ForeignKey로 변경
    bias_group = models.ManyToManyField(
        Group, 
        blank=True, 
        
        related_name='fans_group', # 역참조 이름
        verbose_name="최애 그룹"
    )
    
    # bias_member 필드를 Member 모델을 참조하는 ForeignKey로 변경
    bias_member = models.ManyToManyField(
        Member, 
        blank=True, 
       
        related_name='fans_member', # 역참조 이름
        verbose_name="최애 멤버"
    )
    
    phone = models.CharField(
        max_length=20, blank=True, default='', verbose_name="전화번호"
    )
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="주소")
    state = models.IntegerField(
        choices=USER_STATE_CHOICES, default=1, verbose_name="사용자 상태"
    )
    manners_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        verbose_name="매너 온도"
    )
    nickname = models.CharField(max_length=100, unique=True, verbose_name="닉네임")
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True, verbose_name="프로필 이미지")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="가입일")
    agree_marketing = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="최근 수정일")
    introduction = models.TextField(blank=True, null=True, max_length=100)
    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nickname} ({self.user_id})"


class UserRelation(models.Model):
    # User 모델이 변경되었으므로 from django.conf import settings 후 settings.AUTH_USER_MODEL을 사용하는 것이 안전하나,
    # 여기서는 User 모델이 직접 정의되었으므로 그대로 User를 사용합니다.
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_relations',
        verbose_name="관계 시작 사용자"
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_relations',
        verbose_name="관계 대상 사용자"
    )
    RELATION_CHOICES = [
        ('FOLLOW', '관심 사용자'),
        ('BLOCK', '차단한 사용자'),
    ]
    relation_type = models.CharField(
        max_length=10,
        choices=RELATION_CHOICES,
        verbose_name="관계 유형"
    )

    class Meta:
        unique_together = ('from_user', 'to_user', 'relation_type')
        verbose_name = "사용자 관계"
        verbose_name_plural = "사용자 관계 목록"

    def __str__(self):
        return f"{self.from_user.user_id}가 {self.to_user.user_id}를 {self.get_relation_type_display()}"