# recommend/views.py
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from .gpt_client import call_gpt
from .tmdb_client import enrich_movies, get_movie_details
from .prompt_builder import build_prompt
from .serializers import RecommendationRequestSerializer
from accounts.models import CustomUser, WatchHistory
from core.models import Movie

class RecommendationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RecommendationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_input = serializer.validated_data["input"]

        # 1. 사용자 정보
        username = None
        preferred_genres = []
        watched_titles = []

        if request.user.is_authenticated:
            user = request.user
            username = user.username

            # 선호 장르 추출 (우선순위 순)
            preferred_genres = list(
                user.genre_preferences.select_related("genre")
                .order_by("priority")
                .values_list("genre__name", flat=True)
            )

            # 시청 기록 (최근 300개까지 title 리스트로)
            tmdb_ids = WatchHistory.objects.filter(user=user)
            tmdb_ids = tmdb_ids.order_by("-watched_at").values_list("tmdb_id", flat=True)[:300]
            watched_titles = list(
                Movie.objects.filter(id__in=tmdb_ids).values_list("title", flat=True)
            )

        # 2. 프롬프트 구성
        prompt = build_prompt(
            user_input,
            username=username,
            preferred_genres=preferred_genres,
            watch_history=watched_titles,
        )

        # 3. GPT 호출
        try:
            model = request.data.get("model", "gpt-3.5-turbo")
            gpt_response_text = call_gpt(prompt, model)
            parsed = json.loads(gpt_response_text)
            explanation = parsed.get("explanation", "")
            gpt_result = parsed.get("recommendations", [])

        except Exception as e:
            return Response({"error": f"GPT 응답 처리 실패: {str(e)}"}, status=500)

        # 4. TMDB enrich
        enriched = enrich_movies(gpt_result)

        return Response({
            "explanation": explanation,
            "results": enriched
        })


@api_view(['GET'])
def tmdb_detail(request, movie_id):
    data = get_movie_details(movie_id)
    if data:
        return Response(data)
    return Response({'detail': 'TMDB fetch failed'}, status=502)
