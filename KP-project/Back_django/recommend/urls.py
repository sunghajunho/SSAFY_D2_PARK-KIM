# recommend/urls.py
from django.urls import path
from .views import RecommendationAPIView, tmdb_detail, tmdb_search
from .youtube_views import youtube_search
from .views import default_recommendation

urlpatterns = [
    path('', RecommendationAPIView.as_view(), name='recommendation'),
    path('tmdb/<int:movie_id>/', tmdb_detail),
    path('tmdb/search/', tmdb_search),
    path('youtube/search/', youtube_search),
    path('default/', default_recommendation),
]
