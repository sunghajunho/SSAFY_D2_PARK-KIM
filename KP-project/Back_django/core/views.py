from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Movie, Genre
from .serializers import GenreSerializer
# Create your views here.
def home(request):
    return render(request,'core/home.html')

@api_view(['GET'])
def search_movie(request):
    title = request.GET.get('title', '')
    movies = Movie.objects.filter(title__icontains=title)

    results = [
        {
            'id': movie.id,
            'title': movie.title,
            'genres': [genre.name for genre in movie.genres.all()]
        }
        for movie in movies
    ]

    return Response(results)

class GenreListView(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)