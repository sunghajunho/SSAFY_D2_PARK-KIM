# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .prompt_builder import build_prompt
from .gpt_client import call_gpt, parse_movie_titles
from .tmdb_client import enrich_movies
from .serializers import RecommendationRequestSerializer, RecommendationResponseSerializer

class RecommendationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RecommendationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_input = serializer.validated_data["input"]

        prompt = build_prompt(user_input, user=request.user)
        gpt_response = call_gpt(prompt)
        movie_titles = parse_movie_titles(gpt_response)
        enriched_movies = enrich_movies(movie_titles)

        return Response({"results": enriched_movies})
