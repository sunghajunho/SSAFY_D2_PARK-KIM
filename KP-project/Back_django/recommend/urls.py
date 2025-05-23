# recommend/urls.py
from django.urls import path
from .views import RecommendationAPIView, tmdb_detail

urlpatterns = [
    path('', RecommendationAPIView.as_view(), name='recommendation'),
    path('tmdb/<int:movie_id>/', tmdb_detail),
]
