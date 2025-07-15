from django.db import models
from signupFT.models import User
from idols.models import Member

# 꾸민 포카 한 건
class DecoratedPhotocard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="decorated_photocards")
    title = models.CharField("포카 이름", max_length=100)
    base_image = models.ImageField("원본 포카", upload_to="decorated/base/")
    result_image = models.ImageField("꾸민 이미지 결과", upload_to="decorated/result/", blank=True, null=True)
    
    brightness = models.IntegerField("밝기", default=100)
    contrast = models.IntegerField("대비", default=100)
    saturation = models.IntegerField("채도", default=100)
    
    frame_style = models.CharField("프레임 스타일", max_length=20, choices=[
        ('heart', '하트'), ('star', '별'), ('circle', '원형'),
        ('vintage', '빈티지'), ('polaroid', '폴라로이드'), ('ornate', '화려한')
    ], blank=True, null=True)

    border_color = models.CharField("테두리 색상", max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    # 멤버
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="decorated_photocards", null=True)
    # 태그
    tag = models.CharField(max_length=100, null=True, blank=True)
    # 조회수
    hit = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f"{self.user} - {self.title}"
    
class StickerPlacement(models.Model):
    photocard = models.ForeignKey('DecoratedPhotocard', on_delete=models.CASCADE, related_name="stickers")
    emoji = models.CharField("스티커 이모지", max_length=10)
    x = models.FloatField("X 좌표 (%)")
    y = models.FloatField("Y 좌표 (%)")
    scale = models.FloatField("크기 배율", default=1.0)
    rotation = models.FloatField("회전 각도", default=0.0)

    def __str__(self):
        return f"Sticker {self.emoji} on {self.photocard.title}"
    
    
# 데코 포토카드 위시
class DecoWish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deco_wished_photocards')
    DecoratedPhotocard = models.ForeignKey(DecoratedPhotocard, on_delete=models.CASCADE, related_name='wished_by_users')
    class Meta:
        unique_together = ('user', 'DecoratedPhotocard')
    
    def __str__(self):
        return f'{self.user.user_id} | {self.DecoratedPhotocard.id}'