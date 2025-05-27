# recommend/views.py
import os
import json
import random
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .gpt_client import call_gpt
from .tmdb_client import enrich_movies, get_movie_details, get_recommendations, get_watch_providers
from .prompt_builder import build_prompt
from .serializers import RecommendationRequestSerializer
from accounts.models import CustomUser, WatchHistory
from core.models import Movie

# JSON 파일 경로
data_dir = os.path.join(settings.BASE_DIR, 'recommend', 'data')
POPULAR_PATH = os.path.join(data_dir, 'popular_movies.json')
GENRE_PATH = os.path.join(data_dir, 'genre_pools.json')

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
        print(prompt)

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
    # 로컬 DB에 없으면 TMDB → DB 저장
    if not Movie.objects.filter(id=movie_id).exists():
        movie_data = get_movie_details(movie_id)
        if movie_data:
            from django.db import transaction
            from core.models import Genre
            with transaction.atomic():
                movie, _ = Movie.objects.update_or_create(
                    id=movie_data["id"],
                    defaults={
                        "title": movie_data.get("title"),
                        "overview": movie_data.get("overview", ""),
                        "poster_path": movie_data.get("poster_path"),
                        "release_date": movie_data.get("release_date") or None,
                        "vote_average": movie_data.get("vote_average") or 0,
                        "runtime": movie_data.get("runtime") or 0,
                        "adult": movie_data.get("adult", False),
                        "original_language": movie_data.get("original_language", "en"),
                    },
                )
                genre_ids = [g["id"] for g in movie_data.get("genres", [])]
                if genre_ids:
                    movie.genres.set(genre_ids)
    
    data = get_movie_details(movie_id)
    if not data:
        return Response({'detail': 'TMDB fetch failed'}, status=502)

    related = get_recommendations(movie_id)
    providers = get_watch_providers(movie_id)

    data["related_movies"] = related
    data["watch_providers"] = providers  # flatrate, link 포함됨

    return Response(data)

@api_view(['GET'])
def tmdb_search(request):
    from .tmdb_client import search_movies_by_title
    title = request.GET.get('title', '').strip()
    if not title:
        return Response([])

    movies = search_movies_by_title(title)
    # 필요한 필드만 추려서 응답
    cleaned = [
        {
            "id": m.get("id"),
            "title": m.get("title"),
            "poster_path": m.get("poster_path"),
            "overview": m.get("overview", ""),
            "vote_average": m.get("vote_average", 0),
        }
        for m in movies
    ]
    return Response(cleaned)

@api_view(['GET'])
@permission_classes([AllowAny])
def default_recommendation(request):
    """회원/비회원 분기 추천 API (여러 ID 반환)"""
    try:
        with open(POPULAR_PATH, encoding='utf-8') as f:
            popular_ids = json.load(f)
        with open(GENRE_PATH, encoding='utf-8') as f:
            genre_pools = json.load(f)
    except Exception as e:
        return Response({"error": f"추천 데이터를 불러올 수 없습니다: {str(e)}"}, status=500)

    count = int(request.GET.get('count', 8))  # 기본 8개
    user = request.user if request.user.is_authenticated else None

    if not user:
        # ✅ 비회원: 인기작에서 count개 랜덤
        sampled = random.sample(popular_ids, min(count, len(popular_ids)))
        return Response({"ids": sampled})

    # ✅ 회원: 선호 장르 기반 비율 추출
    prefs = user.genre_preferences.order_by('priority')[:3]
    genre_names = [p.genre.name for p in prefs]
    weights = [40, 35, 25][:len(genre_names)]

    candidate_ids = []
    for name, weight in zip(genre_names, weights):
        pool = genre_pools.get(name, [])
        if pool:
            k = round(weight / 100 * count)
            candidate_ids.extend(random.choices(pool, k=k))

    if not candidate_ids:
        sampled = random.sample(popular_ids, min(count, len(popular_ids)))
    else:
        sampled = random.sample(candidate_ids, min(count, len(candidate_ids)))

    return Response({"ids": sampled})
