from django.db import models

# Create your models here.
class Genre(models.Model):
    id = models.IntegerField(primary_key=True)  # TMDB 장르 ID
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)  # TMDB 영화 ID
    title = models.CharField(max_length=200)  # 영화 제목
    overview = models.TextField()  # 영화 소개
    poster_path = models.CharField(max_length=300)  # 포스터 경로
    release_date = models.DateField(null=True)  # 개봉일
    vote_average = models.FloatField()  # 평균 평점
    runtime = models.PositiveIntegerField(null=True)  # 상영시간(분)
    adult = models.BooleanField()  # 청불 여부
    original_language = models.CharField(max_length=10)  # 원어

    # 장르 연결 (ManyToMany)
    genres = models.ManyToManyField(Genre, related_name='movies_genre')

    def __str__(self):
        return self.title
    