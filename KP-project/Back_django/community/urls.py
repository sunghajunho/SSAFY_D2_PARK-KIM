from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CommentViewSet, UserArticlesView, UserCommentsView, WordcloudView

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('articles/<int:article_pk>/comments/', CommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('articles/<int:pk>/like/', ArticleViewSet.as_view({'post': 'like'})),
    path('articles/<int:article_pk>/comments/<int:pk>/', CommentViewSet.as_view({
        'put': 'update',
        'delete': 'destroy'
    })),
    path('articles/<int:article_pk>/comments/<int:pk>/like/', CommentViewSet.as_view({
        'post': 'like'
    })),
    path('<str:username>/posts/', UserArticlesView.as_view(), name='user-articles'),
    path('<str:username>/comments/', UserCommentsView.as_view(), name='user-comments'),
    path('api/wordcloud/<str:username>/', WordcloudView.as_view(), name='wordcloud'),
]
