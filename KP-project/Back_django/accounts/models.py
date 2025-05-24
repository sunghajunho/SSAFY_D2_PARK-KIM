from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import Genre

class CustomUser(AbstractUser):
    # 사용자 기본 정보 확장
    real_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=30,unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('남성', '남성'), ('여성', '여성')
    ], null=True, blank=True)
    # MBTI
    MBTI_CHOICES = [
        ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('INFJ', 'INFJ'), ('INTJ', 'INTJ'),
        ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('INFP', 'INFP'), ('INTP', 'INTP'),
        ('ESTP', 'ESTP'), ('ESFP', 'ESFP'), ('ENFP', 'ENFP'), ('ENTP', 'ENTP'),
        ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'), ('ENFJ', 'ENFJ'), ('ENTJ', 'ENTJ'),
    ]
    mbti = models.CharField(
        max_length=4,
        choices=MBTI_CHOICES,
        null=True,
        blank=True
    )
    REGION_CHOICES = [
        ('서울', '서울'), ('부산', '부산'), ('대구', '대구'), ('인천', '인천'),
        ('광주', '광주'), ('대전', '대전'), ('울산', '울산'), ('세종', '세종'),
        ('경기', '경기'), ('강원', '강원'), ('충북', '충북'), ('충남', '충남'),
        ('전북', '전북'), ('전남', '전남'), ('경북', '경북'), ('경남', '경남'),
        ('제주', '제주'),
    ]
    region = models.CharField(
        max_length=10,
        choices=REGION_CHOICES,
        null=True,
        blank=True
    )
    # 선호 장르 (ManyToMany → Genre 모델 필요)
    preferred_genres = models.ManyToManyField(Genre,blank=True,through='UserGenrePreference', related_name='user_genre')
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

class UserGenrePreference(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='genre_preferences')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    
    # 순위 필드 추가!
    priority = models.PositiveSmallIntegerField()  # 1, 2, 3 등
    
    class Meta:
        unique_together = ('user', 'genre')
        ordering = ['priority']

class WatchHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="watch_history")
    tmdb_id = models.PositiveIntegerField()
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tmdb_id')
