from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    # 사용자 기본 정보 확장
    nickname = models.CharField(max_length=30, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', '남성'), ('female', '여성'), ('other', '기타')
    ], null=True, blank=True)

    # 선호 장르 (ManyToMany → Genre 모델 필요)
    # 감정 태그 (ManyToMany → EmotionTag 모델 필요)
    # 시청기록은 WatchHistory로 분리 관리 (다대다 중간 테이블)

    # UI 구성용 메서드
    def __str__(self):
        return self.username

class Follow(models.Model):
    follower = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['follower', 'following']