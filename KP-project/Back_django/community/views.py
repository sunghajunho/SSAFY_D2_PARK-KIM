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
    authentication_classes = [TokenAuthentication]  # ✅ 추가됨

    def get_serializer_context(self):  # ✅ context에 request 추가
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    # @action(detail=True, methods=['post'],authentication_classes = [TokenAuthentication],permission_classes=[permissions.IsAuthenticated])
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)

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
            Q(title__icontains=q) | Q(content__icontains=q) | Q(genre__icontains=q) | Q(author__username__icontains=q)
        )
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, TokenAuthentication]  # ✅ 추가됨

    def get_serializer_context(self):  # ✅ context에 request 추가
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

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

