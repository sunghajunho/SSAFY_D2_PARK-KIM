import requests

TMDB_API_KEY = "your_tmdb_api_key"
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"

def enrich_movies(titles: list) -> list:
    enriched = []
    for title in titles:
        response = requests.get(TMDB_SEARCH_URL, params={
            "api_key": TMDB_API_KEY,
            "query": title,
            "language": "ko-KR"
        })
        data = response.json()
        if data["results"]:
            enriched.append(data["results"][0])  # 첫 번째 결과만 사용
    return enriched
