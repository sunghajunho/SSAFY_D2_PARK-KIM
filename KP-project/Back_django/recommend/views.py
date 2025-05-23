import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .gpt_client import call_gpt
from .tmdb_client import enrich_movies, get_movie_details
from .prompt_builder import build_prompt  # 없으면 직접 함수 만들어도 됨
from .serializers import RecommendationRequestSerializer
from rest_framework.decorators import api_view

class RecommendationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RecommendationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_input = serializer.validated_data["input"]

        # 1. 프롬프트 구성 (사용자 기반이면 여기서 username 같이 넘김)
        username = request.user.username if request.user.is_authenticated else None
        prompt = build_prompt(user_input, user=username)

        # 2. GPT 호출
        try:
            gpt_response_text = call_gpt(prompt)
            gpt_result = json.loads(gpt_response_text)
        except Exception as e:
            return Response({"error": f"GPT 응답 처리 실패: {str(e)}"}, status=500)

        # 3. TMDB enrich
        enriched = enrich_movies(gpt_result)

        return Response({"results": enriched})

@api_view(['GET'])
def tmdb_detail(request, movie_id):
    data = get_movie_details(movie_id)
    if data:
        return Response(data)
    return Response({'detail': 'TMDB fetch failed'}, status=502)