from django.db.models.functions import Replace
from django.db.models import F, Value, Q
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Movie, Genre
from .serializers import GenreSerializer, MovieSerializer
# Create your views here.
def home(request):
    return render(request,'core/home.html')

from recommend.tmdb_client import search_movie_by_title, get_movie_details
from django.db import transaction

@api_view(['GET'])
def search_movie(request):
    title = request.GET.get('title', '').strip()
    if not title:
        return Response([])

    clean_query = title.replace(' ', '')

    movies = Movie.objects.annotate(
        clean_title=Replace(F('title'), Value(' '), Value(''))
    ).filter(
        Q(title__icontains=title) | Q(clean_title__icontains=clean_query)
    ).distinct()

    if movies.exists():
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


    # ② TMDB 검색
    movie_data = search_movie_by_title(title)
    if not movie_data:
        return Response([])

    # ③ TMDB 상세정보 (출연진 등 포함)
    details = get_movie_details(movie_data["id"]) or movie_data

    # ④ 로컬 DB에 저장
    with transaction.atomic():
        movie, _ = Movie.objects.update_or_create(
            id=details["id"],
            defaults={
                "title": details.get("title") or details.get("original_title") or title,
                "overview": details.get("overview", ""),
                "poster_path": details.get("poster_path"),
                "release_date": details.get("release_date") or None,
                "vote_average": details.get("vote_average") or 0,
                "runtime": details.get("runtime") or 0,
                "adult": details.get("adult", False),
                "original_language": details.get("original_language", "en"),
            },
        )
        genre_ids = details.get("genre_ids") or [g["id"] for g in details.get("genres", [])]
        if genre_ids:
            movie.genres.set(genre_ids)

    # ⑤ 응답
    serializer = MovieSerializer([movie], many=True)
    return Response(serializer.data)


@api_view(['GET'])
def suggest_movies(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 1:
        return Response([])

    suggestions = Movie.objects.filter(title__icontains=query).values('id', 'title')[:10]
    return Response(list(suggestions))


class GenreListView(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)
    
