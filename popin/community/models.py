from django.db import models
from django.conf import settings
from signupFT.models import User
from django.utils import timezone


class Board(models.Model):
    TYPE_CHOICES = [
        ('exchange-review', '교환후기'),
        ('offline-sharing', '나눔'),
        ('offline-proxy', '대리구매'),
        ('offline-status', '현황 공유'),
        ('offline-companion', '동행'),
        ('recent-activity', '최근 활동'),
    ]
    board_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    icon = models.CharField(max_length=10, default='⭐')
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    description = models.TextField()
    features = models.TextField(help_text="특징 리스트를 줄바꿈으로 구분")
    stat_total = models.CharField(max_length=50)
    stat_label_total = models.CharField(max_length=50)
    stat_secondary = models.CharField(max_length=50, blank=True, null=True)
    stat_label_secondary = models.CharField(max_length=50, blank=True, null=True)
    stat_tertiary = models.CharField(max_length=50, blank=True, null=True)
    stat_label_tertiary = models.CharField(max_length=50, blank=True, null=True)
    write_url = models.URLField(blank=True, null=True)
    view_url = models.URLField(blank=True, null=True)

    def feature_list(self):
        return self.features.split('\n')

    def stats(self):
        stats = []
        if self.stat_total and self.stat_label_total:
            stats.append({'number': self.stat_total, 'label': self.stat_label_total})
        if self.stat_secondary and self.stat_label_secondary:
            stats.append({'number': self.stat_secondary, 'label': self.stat_label_secondary})
        if self.stat_tertiary and self.stat_label_tertiary:
            stats.append({'number': self.stat_tertiary, 'label': self.stat_label_tertiary})
        return stats

    def __str__(self):
        return self.title
    
    

    ##################################################################


# 후기 태그
class ReviewTag(models.Model):
    name = models.CharField("태그명", max_length=30, unique=True)

    def __str__(self):
        return self.name

# 후기 모델
class ExchangeReview(models.Model):
    title = models.CharField("제목", max_length=100)
    content = models.TextField("후기 내용")
    
    # 작성자와 교환 상대방
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="written_reviews", verbose_name="작성자")
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_reviews", verbose_name="교환 상대방")

    tags = models.ManyToManyField(ReviewTag, blank=True, related_name="reviews", verbose_name="태그")
    artist = models.CharField("아티스트", max_length=50,default="기타")
    method = models.CharField("교환 방식", max_length=20, choices=[("온라인", "온라인"), ("오프라인", "오프라인")])
    transaction_type = models.CharField("거래 방식", max_length=10, choices=[("교환", "교환"), ("양도", "양도")], default="교환")

    overall_score = models.PositiveSmallIntegerField("총 평점 (1~5)", choices=[(i, f"{i}점") for i in range(1, 6)])

    created_at = models.DateTimeField("작성일", auto_now_add=True)
    views = models.PositiveIntegerField("조회수", default=0)

    def __str__(self):
        return f"[{self.title}] {self.writer} → {self.partner}"

# 이미지
class ReviewImage(models.Model):
    review = models.ForeignKey(ExchangeReview, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField("첨부 이미지", upload_to='review_images/')
    caption = models.CharField("이미지 설명", max_length=100, blank=True)
    uploaded_at = models.DateTimeField("업로드 시간", auto_now_add=True)

    def __str__(self):
        return f"Image for {self.review.title}"
    
#######################################################################


# 동행 카테고리 (콘서트, 팬미팅 등)
class CompanionCategory(models.TextChoices):
    CONCERT = '콘서트', '콘서트'
    FANSIGN = '팬사인회', '팬사인회'
    POPUP = '팝업스토어', '팝업스토어'
    EXHIBITION = '전시회', '전시회'
    GOODS = '굿즈샵', '굿즈샵'
    ETC = '기타', '기타'
    
# 태그  
class CompanionTag(models.Model):
    name = models.CharField("태그명", max_length=30, unique=True)

    def __str__(self):
        return self.name
    
# 동행 모집 게시글

class CompanionPost(models.Model):
    title = models.CharField("제목", max_length=100)
    content = models.TextField("본문")

    category = models.CharField("카테고리", max_length=20, choices=CompanionCategory.choices)
    artist = models.CharField("아티스트", max_length=50)

    event_date = models.DateTimeField("행사 날짜 및 시간")
    location = models.CharField("위치", max_length=100)

    max_people = models.PositiveIntegerField("최대 모집 인원")
    participants = models.ManyToManyField(
        User,
        blank=True,
        related_name="joined_companions",
        verbose_name="참여자 목록"
    )

    status = models.CharField(
        "모집 상태",
        max_length=10,
        choices=[('모집중', '모집중'), ('모집완료', '모집완료'),('진행중', '진행중')],
        default='모집중'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="companion_posts",
        verbose_name="작성자"
    )

    created_at = models.DateTimeField("작성일", auto_now_add=True)
    views = models.PositiveIntegerField("조회수", default=0)
    comments_count = models.PositiveIntegerField("댓글 수", default=0)

    def __str__(self):
        return f"[{self.artist}] {self.title}"

    @property
    def current_people(self):
        return self.participants.count()

    @property
    def status_display_with_count(self):
        return f"{self.current_people}/{self.max_people} ({self.status})"

# 댓글 모델 (선택)
class CompanionComment(models.Model):
    post = models.ForeignKey(CompanionPost, on_delete=models.CASCADE, related_name="comments", verbose_name="게시글")
    content = models.TextField("댓글 내용")
    created_at = models.DateTimeField("작성일", auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.content[:20]}"
    
    
    
class CompanionImage(models.Model):
    post = models.ForeignKey(CompanionPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField("첨부 이미지", upload_to='companion_images/')
    caption = models.CharField("이미지 설명", max_length=100, blank=True)
    uploaded_at = models.DateTimeField("업로드 시간", auto_now_add=True)

    def __str__(self):
        return f"{self.post.title}의 이미지"
    
    
    
    ########################################

# --- 카테고리, 상태 Choice ---
class ProxyCategory(models.TextChoices):
    ALBUM = '앨범', '앨범'
    PHOTOCARD = '포토카드', '포토카드'
    GOODS = '굿즈', '굿즈'
    CONCERT = '콘서트', '콘서트'


class ProxyStatus(models.TextChoices):
    RECRUITING = '모집중', '모집중'
    URGENT = '긴급모집', '긴급모집'
    DEADLINE = '마감임박', '마감임박'


# --- 태그 모델 ---
class ProxyTag(models.Model):
    name = models.CharField("태그명", max_length=30, unique=True)

    def __str__(self):
        return self.name


# --- 대리구매 게시글 ---
class ProxyPost(models.Model):
    title = models.CharField("제목", max_length=100)
    artist = models.CharField("아티스트", max_length=50)  # 예: aespa, NCT DREAM
    category = models.CharField("카테고리", max_length=20, choices=ProxyCategory.choices)
    status = models.CharField("모집상태", max_length=20, choices=ProxyStatus.choices)

    event_date = models.DateTimeField("이벤트 날짜 및 시간")
    location = models.CharField("장소", max_length=100)

    max_people = models.PositiveIntegerField("최대 모집 인원")
    participants = models.ManyToManyField(User, blank=True, related_name="joined_proxies", verbose_name="참여자 목록")
    

    reward = models.CharField("수고비", max_length=100)  # 예: '개당 수고비 0.1'
    description = models.TextField("본문")

    tags = models.ManyToManyField(ProxyTag, blank=True, related_name="proxy_posts", verbose_name="태그")
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name="proxy_posts", verbose_name="작성자")
   
    created_at = models.DateTimeField("작성일", auto_now_add=True)

    views = models.PositiveIntegerField("조회수", default=0)
    comments_count = models.PositiveIntegerField("댓글 수", default=0)

    def __str__(self):
        return f"[{self.artist}] {self.title}"

    @property
    def current_people(self):
        return self.participants.count()
    
    @property
    def status_display_with_count(self):
        return f"{self.current_people}/{self.max_people} ({self.status})"
    

# --- 댓글 모델 ---
class ProxyComment(models.Model):
    post = models.ForeignKey(ProxyPost, on_delete=models.CASCADE, related_name='comments', verbose_name="게시글")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    content = models.TextField("댓글 내용")
    created_at = models.DateTimeField("작성일", auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.content[:20]}"       
     
class ProxyImage(models.Model):
    post = models.ForeignKey(ProxyPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField("첨부 이미지", upload_to='proxy_images/')
    caption = models.CharField("이미지 설명", max_length=100, blank=True)
    uploaded_at = models.DateTimeField("업로드 시간", auto_now_add=True)

    def __str__(self):
        return f"{self.post.title}의 이미지"    
################################################

class SharingTag(models.Model):
    name = models.CharField("태그명", max_length=30, unique=True)

    def __str__(self):
        return self.name


class SharingPost(models.Model):
    CATEGORY_CHOICES = [
        ('앨범', '앨범'),
        ('굿즈', '굿즈'),
        ('기타', '기타'),
    ]

    TYPE_CHOICES = [
        ('온라인', '온라인'),
        ('오프라인', '오프라인'),
    ]

    title = models.CharField("제목", max_length=100)
    content = models.TextField("내용")
    artist = models.CharField("아티스트", max_length=50,default="기타")
    requirement=models.TextField("필수사항")
    category = models.CharField("카테고리", max_length=20, choices=CATEGORY_CHOICES)
    type = models.CharField("나눔 형태", max_length=10, choices=TYPE_CHOICES)

    share_date = models.DateTimeField("나눔 날짜", default=timezone.now)
    location = models.CharField("나눔 장소", max_length=100, blank=True)

    tags = models.ManyToManyField(SharingTag, blank=True, related_name="sharing_posts", verbose_name="태그")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sharing_posts", verbose_name="작성자")


    created_at = models.DateTimeField("작성일", auto_now_add=True)
    views = models.PositiveIntegerField("조회수", default=0)

    def __str__(self):
        return f"[{self.title}] by {self.author}"


class SharingImage(models.Model):
    post = models.ForeignKey(SharingPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField("첨부 이미지", upload_to='sharing_images/')
    uploaded_at = models.DateTimeField("업로드 시각", auto_now_add=True)

    def __str__(self):
        return f"{self.post.title}의 이미지"