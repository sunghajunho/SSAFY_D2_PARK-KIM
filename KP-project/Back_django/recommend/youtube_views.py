# recommend/youtube_views.py

import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

@api_view(['GET'])
def youtube_search(request):
    title = request.GET.get("title")
    category = request.GET.get("category", "리뷰")  # ex: 리뷰, 쇼츠

    if not title:
        return JsonResponse({"error": "title 파라미터가 필요합니다."}, status=400)

    q = f"{title} {category}"
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": YOUTUBE_API_KEY,
        "q": q,
        "type": "video",
        "maxResults": 6,
        "part": "snippet",
    }

    res = requests.get(url, params=params)
    if res.status_code != 200:
        return JsonResponse({"error": "YouTube API 요청 실패"}, status=502)

    items = res.json().get("items", [])
    videos = [
        {
            "title": item["snippet"]["title"],
            "videoId": item["id"]["videoId"],
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
            "channel": item["snippet"]["channelTitle"],
        }
        for item in items
    ]
    return Response(videos)
