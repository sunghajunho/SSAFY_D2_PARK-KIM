from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('articles/<int:article_pk>/comments/', CommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('articles/<int:article_pk>/comments/<int:pk>/', CommentViewSet.as_view({
        'put': 'update',
        'delete': 'destroy'
    })),
]
