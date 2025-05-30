from django.db import models
from django.conf import settings
from core.models import Genre, Movie

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=100)
    content = models.TextField()
    movie_title = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='articles')
    genre = models.ManyToManyField(Genre, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    article_likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles', blank=True)

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    comment_likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_comments',
        blank=True
    )


