from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.author == request.user

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    authentication_classes = [SessionAuthentication, TokenAuthentication]  # ✅ 추가됨

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        article = self.get_object()
        article.article_likes += 1
        article.save()
        return Response({'article_likes': article.article_likes})

    @action(detail=False)
    def search(self, request):
        q = request.query_params.get('q', '')
        qs = self.get_queryset().filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(genre__icontains=q) | Q(author__username__icontains=q)
        )
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    authentication_classes = [SessionAuthentication, TokenAuthentication]  # ✅ 추가됨

    def get_queryset(self):
        return Comment.objects.filter(article_id=self.kwargs['article_pk'], parent=None)

    def create(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=self.kwargs['article_pk'])
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("🚨 serializer.errors:", serializer.errors)  # 여기!
            return Response(serializer.errors, status=400)
        serializer.save(author=request.user, article=article)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

