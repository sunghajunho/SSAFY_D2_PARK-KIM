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

    # ✅ 원래 ForeignKey 필드 (id 저장용)
    movie_title = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all()
    )

    # ✅ 영화 제목을 보여주기 위한 read-only 필드
    movie_title_display = serializers.SerializerMethodField()

    genre = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all()
    )
    article_likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['author', 'article_likes', 'views', 'created_at', 'updated_at',]

    def get_movie_title_display(self, obj):
        return obj.movie_title.title if obj.movie_title else None

    def get_article_likes(self, obj):
        return obj.liked_users.count()

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        user = getattr(request, 'user', None)
        if user and request.user.is_authenticated:
            return obj.liked_users.filter(pk=request.user.pk).exists()
        return False