from django.db import models
from django.utils import timezone
from signupFT.models import User 

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