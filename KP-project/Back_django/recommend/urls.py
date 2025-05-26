# recommend/urls.py
from django.urls import path
from .views import RecommendationAPIView, tmdb_detail
from .youtube_views import youtube_search

urlpatterns = [
    path('', RecommendationAPIView.as_view(), name='recommendation'),
    path('tmdb/<int:movie_id>/', tmdb_detail),
    path('youtube/search/', youtube_search),
]
