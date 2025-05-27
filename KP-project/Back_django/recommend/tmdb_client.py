import os
import requests
from typing import Optional, Dict, List
from core.models import Movie, Genre
from django.db import transaction


TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"


def search_movie_by_title(title: str) -> Optional[Dict]:
    """제목으로 영화 검색"""
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": "ko-KR",
    }
    res = requests.get(f"{TMDB_BASE_URL}/search/movie", params=params)
    if res.status_code != 200:
        print(f"[TMDB] 검색 실패: {res.text}")
        return None
    results = res.json().get("results", [])
    return results[0] if results else None

def search_movies_by_title(title: str, limit: int = 4) -> List[Dict]:
    """제목으로 유사한 영화 여러 개 반환"""
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": "ko-KR",
    }
    res = requests.get(f"{TMDB_BASE_URL}/search/movie", params=params)
    if res.status_code != 200:
        print(f"[TMDB] 검색 실패: {res.text}")
        return []
    results = res.json().get("results", [])
    return results[:limit]



def get_movie_details(movie_id: int) -> Optional[Dict]:
    """id로 영화 상세정보 + 출연진까지 불러오기"""
    params = {
        "api_key": TMDB_API_KEY,
        "append_to_response": "credits",
        "language": "ko-KR",
    }
    res = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}", params=params)
    if res.status_code != 200:
        print(f"[TMDB] 상세정보 실패: {res.text}")
        return None
    return res.json()


def enrich_movies(gpt_result: List[Dict]) -> List[Dict]:
    """GPT 추천 결과(title만 있음)를 로컬 DB 우선으로 enrich. 없으면 TMDB fallback"""
    enriched = []

    for item in gpt_result:
        title = item["title"].strip()
        reason = item.get("description", "")

        # ① 로컬 DB에서 title 일치 검색 (대소문자 무시)
        movie = Movie.objects.filter(title__iexact=title).first()

        # ② 없으면 TMDB API로 보강
        if not movie:
            movie_data = search_movie_by_title(title)
            if not movie_data:
                # TMDB에서도 못 찾으면 최소한 제목만 반환
                enriched.append({
                    "title": title,
                    "id": None,
                    "poster_path": None,
                    "overview": "",
                    "rating": "정보 없음",
                    "reason": reason,
                })
                continue

            details = get_movie_details(movie_data["id"]) or movie_data

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
                # 장르 연결
                genre_ids = details.get("genre_ids") or [g["id"] for g in details.get("genres", [])]
                if genre_ids:
                    movie.genres.set(genre_ids)

        # 공통 응답 포맷
        enriched.append({
            "title": movie.title,
            "id": movie.id,
            "poster_path": movie.poster_path,
            "overview": movie.overview,
            "rating": movie.vote_average,
            "reason": reason,
        })

    return enriched

def get_recommendations(movie_id: int) -> List[Dict]:
    """TMDB에서 연관 영화 추천 가져오기"""
    params = {
        "api_key": TMDB_API_KEY,
        "language": "ko-KR",
    }
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations"
    res = requests.get(url, params=params)
    if res.status_code != 200:
        print(f"[TMDB] 연관 영화 추천 실패: {res.text}")
        return []

    results = res.json().get("results", [])
    recommendations = []

    for movie in results[:10]:  # 최대 10개까지만 사용
        recommendations.append({
            "id": movie["id"],
            "title": movie.get("title", ""),
            "poster_path": movie.get("poster_path"),
            "overview": movie.get("overview", ""),
            "vote_average": movie.get("vote_average", 0)
        })

    return recommendations

def get_watch_providers(movie_id: int) -> Dict:
    """TMDB에서 OTT 제공처 정보 가져오기"""
    params = {
        "api_key": TMDB_API_KEY,
    }
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/watch/providers"
    res = requests.get(url, params=params)
    if res.status_code != 200:
        print(f"[TMDB] 감상처 정보 실패: {res.text}")
        return {}

    data = res.json().get("results", {})
    return data.get("KR", {})  # 한국 감상처만
