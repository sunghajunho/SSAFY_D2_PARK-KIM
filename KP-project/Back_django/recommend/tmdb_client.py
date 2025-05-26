import os
import requests
from typing import Optional, Dict, List

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
     """GPT가 준 추천 결과(title만 있음)를 TMDB 정보로 풍부하게 만들어줌"""
     enriched = []
     for item in gpt_result:
         movie_data = search_movie_by_title(item["title"])
         if movie_data:
            # 1) ko-KR title   2) original_title   3) GPT가 준 title
            title_ko = (
                movie_data.get("title")          # 번역된 제목
                or movie_data.get("original_title")
                or item["title"]
            )
            enriched.append({
                 "title": title_ko,
                 "id": movie_data["id"],
                 "poster_path": movie_data.get("poster_path"),
                 "overview": movie_data.get("overview", ""),
                 "rating": movie_data.get("vote_average", "N/A"),
                 "reason": item.get("description", ""),
             })
     return enriched