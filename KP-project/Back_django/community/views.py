from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.db.models import Count
from django.shortcuts import get_object_or_404
from .models import Article, Comment
from accounts.models import CustomUser
from .serializers import ArticleSerializer, CommentSerializer
from datetime import datetime, timedelta
from django.db import models

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.author == request.user

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    authentication_classes = [TokenAuthentication]  # ✅ 추가됨

    def get_serializer_context(self):  # ✅ context에 request 추가
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.query_params.get('sort')

        if sort == 'views':
            queryset = queryset.order_by('-views', '-created_at')  # 조회수 높은 순 + 최신순
        elif sort == 'likes':
            queryset = queryset.annotate(num_likes=models.Count('liked_users')).order_by('-num_likes', '-created_at')
        else:  # 기본값: 최신순
            queryset = queryset.order_by('-created_at')

        return queryset
    
    # @action(detail=True, methods=['post'],authentication_classes = [TokenAuthentication],permission_classes=[permissions.IsAuthenticated])
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # 🚀 쿠키 기반 조회수 중복 방지
        cookie_name = f'viewed_article_{instance.id}'
        if not request.COOKIES.get(cookie_name):
            instance.views += 1
            instance.save(update_fields=['views'])

        response = super().retrieve(request, *args, **kwargs)

        # 쿠키 만료시간: 1일 뒤 (브라우저마다 다름)
        expires = datetime.strftime(datetime.utcnow() + timedelta(days=1), "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie(cookie_name, 'true', expires=expires, httponly=True, samesite='Lax',secure=False)
        # print(request.COOKIES)
        return response

    @action(detail=True, methods=['post'],permission_classes=[permissions.IsAuthenticated])  # ✅ detail=True는 pk 기반
    def like(self, request, pk=None):
        article = self.get_object()
        user = request.user

        if article.liked_users.filter(pk=user.pk).exists():
            article.liked_users.remove(user)
            liked = False
        else:
            article.liked_users.add(user)
            liked = True

        return Response({
            'liked': liked,
            'article_likes': article.liked_users.count()
        })

    @action(detail=False)
    def search(self, request):
        q = request.query_params.get('q', '')
        qs = self.get_queryset().filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(genre__name__icontains=q) | Q(author__username__icontains=q) | Q(movie_title__title__icontains=q)
        ).distinct()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]  # ✅ 추가됨

    def get_serializer_context(self):  # ✅ context에 request 추가
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        return Comment.objects.filter(
            article_id=self.kwargs['article_pk'],
            parent=None
        ).annotate(
            num_likes=Count('liked_users')  # ⭐️ 좋아요 수 계산
        ).order_by('-num_likes', 'created_at')  # ⭐️ 좋아요 수 내림차순, 같으면 created_at 오름차순


    def create(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=self.kwargs['article_pk'])
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("🚨 serializer.errors:", serializer.errors)  # 여기!
            return Response(serializer.errors, status=400)
        serializer.save(author=request.user, article=article)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'],permission_classes=[permissions.IsAuthenticated])
    def like(self, request, article_pk=None, pk=None):
        comment = self.get_object()
        print(comment)
        user = request.user

        if comment.liked_users.filter(pk=user.pk).exists():
            comment.liked_users.remove(user)
            liked = False
        else:
            comment.liked_users.add(user)
            liked = True

        return Response({
            'liked':liked,
            'comment_likes': comment.liked_users.count()
        })

class UserArticlesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, username):
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({'detail': '사용자가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        articles = Article.objects.filter(author=user).order_by('-created_at')
        serializer = ArticleSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserCommentsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, username):
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({'detail': '사용자가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(author=user).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def movie_articles(request, movie_id):
    articles = Article.objects.filter(movie_title_id=movie_id).order_by('-created_at')
    serializer = ArticleSerializer(articles, many=True, context={'request': request})
    return Response(serializer.data)
    

# 워드클라우드 용
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from django.http import JsonResponse
from django.views import View
from collections import Counter
import io
import re
import base64
from community.models import Article
from accounts.models import CustomUser

class WordcloudView(View):
    def get(self, request, username):
        # 해당 username의 게시글만 가져오기
        user = CustomUser.objects.get(username=username)
        contents = Article.objects.filter(author=user).values_list('content', flat=True)
        text = ' '.join(contents)

        # 단어 단위 분석
        words = re.findall(r'\b\w+\b', text)
        stopwords = set(['영화', '감상', '감상평'])
        words = [word for word in words if word not in stopwords and len(word) > 1]

        word_freq = Counter(words)
        top_words = dict(word_freq.most_common(10))

        if not top_words:
            top_words = {"데이터 없음": 1}

        # 워드클라우드 생성
        wordcloud = WordCloud(
            font_path='C:/Windows/Fonts/malgun.ttf',
            background_color='white',
            width=800,
            height=400
        ).generate_from_frequencies(top_words)

        buffer = io.BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud.to_array(), interpolation='bilinear')
        plt.axis('off')
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)

        # 🎯 이미지 Base64 인코딩
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # 🎯 취향 파악 문장
        categories = {
            "영상미": ["영상미", "연출", "색감"],
            "스토리": ["스토리", "전개", "결말"],
            "연기력": ["연기", "배우", "캐릭터"],
            "음악": ["OST", "음악", "사운드"],
            "메시지": ["메시지", "사회적", "철학", "감독의 의도"]
        }
        category_scores = {}
        for category, keywords in categories.items():
            score = sum(word_freq.get(keyword, 0) for keyword in keywords)
            category_scores[category] = score

        top_category = max(category_scores, key=category_scores.get)
        category_phrases = {
            "영상미": "영상미를 중시하는 감각파 🎥",
            "스토리": "스토리를 중시하는 몰입파 📚",
            "연기력": "연기력을 중시하는 배우파 🎭",
            "음악": "음악을 중시하는 감성파 🎶",
            "메시지": "메시지를 중시하는 메시지파 💬"
        }
        final_sentence = f"당신은 {category_phrases[top_category]}!"

        # JSON 응답
        return JsonResponse({
            "image": image_base64,
            "description": final_sentence
        })





