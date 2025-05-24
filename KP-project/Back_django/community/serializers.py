from rest_framework import serializers
from .models import Article, Comment  # ✅ 모델 클래스 명시적 import
from django.contrib.auth import get_user_model
from accounts.serializers import CustomUserSerializer
from core.models import Genre, Movie

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    comment_likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'created_at','comment_likes','article',]

        
    def get_replies(self, obj):
        if obj.replies.exists():
            return self.__class__(obj.replies.all(), many=True).data
        return []
    
    def get_comment_likes(self,obj):
        return obj.liked_users.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request',None)
        user = getattr(request,'user',None)
        if user and request.user.is_authenticated:
            return obj.liked_users.filter(pk=request.user.pk).exists()
        return False


class ArticleSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    movie_title = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    genre = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all()
    )
    article_likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Article  # ✅ 문자열이 아닌 클래스 참조로 수정
        fields = '__all__'
        read_only_fields = ['author', 'article_likes', 'views', 'created_at', 'updated_at',]

    def get_movie_genres(self, obj):
        if obj.movie:
            return [genre.name for genre in obj.movie.genres.all()]
        return []
    
    def get_article_likes(self,obj):
        return obj.liked_users.count()
    
    def get_is_liked(self,obj):
        request = self.context.get('request',None)
        user = getattr(request,'user',None)
        if user and request.user.is_authenticated:
            return obj.liked_users.filter(pk=request.user.pk).exists()
        return False