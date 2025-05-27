# generate_movie_pools.py
import os
import json
import requests
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()  # .env에서 TMDB_API_KEY 불러오기
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def get_tmdb(endpoint, params=None):
    url = f"{TMDB_BASE_URL}/{endpoint}"
    params = params or {}
    params["language"] = "ko-KR"
    params["api_key"] = TMDB_API_KEY
    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.json()

def get_genres():
    data = get_tmdb("genre/movie/list")
    return {g["id"]: g["name"] for g in data["genres"]}

def get_popular_movies(count=100):
    movies = []
    page = 1
    while len(movies) < count and page <= 10:
        res = get_tmdb("movie/popular", {"page": page})
        for movie in res["results"]:
            if movie.get("vote_average", 0) >= 7.5:
                movies.append(movie["id"])
            if len(movies) >= count:
                break
        page += 1
    return movies[:count]

def get_genre_popular_movies(genre_ids, per_genre=50):
    genre_pools = defaultdict(list)
    for gid, name in genre_ids.items():
        page = 1
        collected = []
        while len(collected) < per_genre and page <= 5:
            res = get_tmdb("discover/movie", {
                "with_genres": gid,
                "sort_by": "vote_average.desc",
                "vote_count.gte": 100,
                "page": page
            })
            ids = [m["id"] for m in res["results"]]
            collected.extend(ids)
            page += 1
        genre_pools[name] = collected[:per_genre]
    return genre_pools

if __name__ == "__main__":
    genres = get_genres()
    popular = get_popular_movies(100)
    genre_pools = get_genre_popular_movies(genres, per_genre=50)

    with open("popular_movies.json", "w", encoding="utf-8") as f:
        json.dump(popular, f, ensure_ascii=False, indent=2)

    with open("genre_pools.json", "w", encoding="utf-8") as f:
        json.dump(genre_pools, f, ensure_ascii=False, indent=2)

    print("🎉 영화 추천용 ID Pool 생성 완료!")
