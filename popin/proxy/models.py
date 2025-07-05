from django.db import models
from django.conf import settings
from signupFT.models import User

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
    uthor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
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
