from rest_framework import serializers
from .models import Article, Comment  # ✅ 모델 클래스 명시적 import
from django.contrib.auth import get_user_model
from accounts.serializers import CustomUserSerializer

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'created_at','comment_likes','article',]

        
    def get_replies(self, obj):
        if obj.replies.exists():
            return self.__class__(obj.replies.all(), many=True).data
        return []


class ArticleSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    movie_genres = serializers.SerializerMethodField()

    class Meta:
        model = Article  # ✅ 문자열이 아닌 클래스 참조로 수정
        fields = '__all__'
        read_only_fields = ['author', 'article_likes', 'views', 'created_at', 'updated_at',]

    def get_movie_genres(self, obj):
        if obj.movie:
            return [genre.name for genre in obj.movie.genres.all()]
        return []